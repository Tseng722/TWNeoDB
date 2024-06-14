from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from app.form import searchmTSAForm
from os import path, makedirs, getcwd
import os
from django.conf import settings


from app.score import pvac,hydro,similarity,is_pep_in_db
from app.ip import get_location
from app.task import is_path_exist, all_score,test,send_email
from django_q.tasks import async_task
from django_q.tasks import result
from django.db.models import Count,Avg
from django.db.models import Q

# from app.models import mtsa_RNA,aeTSA,annotation,opensource,info_patient,bind_mtsa,annotation_mtsa,bind_aetsa,annotation_aetsa
# from app.models import mtsa_pmhc,mtsa_annotation,mtsa_annotation_detail,patient,mtsa_pmhc_annotation_mapping
# from app.models import mtsa_pmhc_patient_mapping,scoring
from app.models import user_info, user_job
# from app.models import mtsa_dna_annotation,mtsa_dna_score
from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,hla_in_patient
from app.models import aetsa_transcript_mutant_mapping,patient_aetsa_score,aetsa_transcript
from app.models import shared_pep_mtsa_rna,shared_pep_mtsa_dna,shared_pep_aetsa
from app.models import validated_peptide

import json
import requests
# from app.filter import mTSAFilter,mtsaFilter1,aetsaFilter,mtsaFilter

from django.http import FileResponse
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import io
import datetime
import uuid
from ipware import get_client_ip
# from geoip import geolite2
# import geoip2.database
from geolite2 import geolite2
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

import plotly.graph_objects as go
from django.shortcuts import render
from plotly.offline import plot
import plotly.express as px

from django_pandas.io import read_frame

reader = geolite2.reader()
OUT_FILE_DIR= settings.OUTPUT_BASE_DIR
# Create your views here.
global tumor_protein,tissue_type,source,gene_symbol,hla_type

def index(request):
    # distinct_tumor_types = patient_info.objects.values('tumor_type').distinct()
    tumor_type_counts = patient_info.objects.values('tumor_type').annotate(count=Count('id')).order_by('-count')
    total_tumor_count = tumor_type_counts.count()
    total_patient_count = patient_info.objects.count()

    total_hla_count = peptide_selection_score.objects.values('hla_type').distinct().count()
    mtsa_rna_count = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').values('mutant_peptide_id__tumor_protein').distinct().count()
    mtsa_dna_count = mtsa_dna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').values('mutant_peptide_id__tumor_protein').distinct().count()
    aetsa_count = aetsa_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').values('mutant_peptide_id__tumor_protein').distinct().count()
    validated_pep_count = validated_peptide.objects.values('tumor_protein').distinct().count()
    return render(request,"home.html",locals())


def listall(request):
    try:
        mtsa_all = mtsa_RNA.objects.all()
    except:
        errormessage = "(error)"
    return render(request,"table_test1.html",locals())


def search(request):
    if request.method == "POST":
        mess = request.POST['username']
    else:
        mess = "FAIL"
    return render(request, "search_test.html",locals())

def about(request):
    
    return render(request, "about.html",locals())


def sort(request , mode=None):
    if mode =='tumor_sort':
        try:
            mtsa_all = mtsa_RNA.objects.all().order_by('mTumor_protein')
        except:
            errormessage = "(error)"
    return render(request, "table_test1.html",locals())

def file_load_view(request):
    if request.method == 'POST':
        mtsa_all = mtsa_RNA.objects.all()
        print(mtsa_all[1])
    
    return render(request, "search_test.html",locals())
def detail_page_mtsa_dna(request,id):
    source = 'DNA'
    mapping = mtsa_dna_transcript_mutant_mapping.objects.get(id=id)
    mutant_peptide_id = mapping.mutant_peptide_id.id
    transcript_id = mapping.mtsa_dna_transcript_id.id

    tumor_object = mtsa_dna_transcript_mutant_mapping.objects.filter(mutant_peptide_id=mutant_peptide_id,mtsa_dna_transcript_id=transcript_id)
    associated_transcript_object = mtsa_dna_transcript_mutant_mapping.objects.filter(mutant_peptide_id=mutant_peptide_id).exclude(mtsa_dna_transcript_id=transcript_id)
    associated_pep_object = mtsa_dna_transcript_mutant_mapping.objects.filter(mtsa_dna_transcript_id=transcript_id).exclude(mutant_peptide_id=mutant_peptide_id)
    

    mutant_peptide_object = mutant_peptide.objects.get(id = mutant_peptide_id)
    patient_transcript_score_object = patient_transcript_score.objects.filter(dna_id = transcript_id)
    transcript_object = mtsa_dna_transcript.objects.get(id = transcript_id)
    validated_peptide = mutant_peptide_object.peptide_selection_score_id.validated_peptide_id
    score_groupby = patient_transcript_score_object.values('dna_id').annotate(
        tpm_n_avg=Avg('tpm_normal'),
        tpm_t_avg=Avg('tpm_tumor'),
        fold_change_avg=Avg('fold_change'),
        tumor_dna_depth_avg=Avg('tumor_dna_depth'),
        tumor_dna_vaf_avg=Avg('tumor_dna_vaf'))

    tumor = mutant_peptide_object.tumor_protein
    normal = mutant_peptide_object.normal_protein
    hla = mutant_peptide_object.hla_type
    pos = mutant_peptide_object.pos
    try :
        r = requests.get(f'https://query-api.iedb.org/mhc_search?linear_sequence=eq.{tumor}&select=linear_sequence%2Cstructure_type%2Csource_organism_name%2Celution_id%2Cmhc_restriction%2Cqualitative_measure%2Chost_organism_name%2Cmhc_allele_name')
        dict_obj = json.loads(r.text)
        
    except:
        pass
    return render(request,"detail_page_mtsa_dna.html",locals())
    

def detail_page_mtsa(request,id):
    source = 'RNA'
    mapping = mtsa_rna_transcript_mutant_mapping.objects.get(id=id)
    print(id)
    mutant_peptide_id = mapping.mutant_peptide_id.id
    transcript_id = mapping.mtsa_rna_transcript_id.id
    mutant_peptide_object = mutant_peptide.objects.get(id = mutant_peptide_id)
    # rna_ids_list = mtsa_rna_transcript_mutant_mapping.objects.filter(mutant_peptide_id=mutant_peptide_id).values_list('mtsa_rna_transcript_id', flat=True)
    # patient_transcript_score_object = patient_transcript_score.objects.filter(rna_id__in=rna_ids_list)
    
    tumor_object = mtsa_rna_transcript_mutant_mapping.objects.filter(mutant_peptide_id=mutant_peptide_id,mtsa_rna_transcript_id=transcript_id)
    associated_transcript_object = mtsa_rna_transcript_mutant_mapping.objects.filter(mutant_peptide_id=mutant_peptide_id).exclude(mtsa_rna_transcript_id=transcript_id)
    associated_pep_object = mtsa_rna_transcript_mutant_mapping.objects.filter(mtsa_rna_transcript_id=transcript_id).exclude(mutant_peptide_id=mutant_peptide_id)
    
    patient_transcript_score_object = patient_transcript_score.objects.filter(rna_id = transcript_id)
    score_groupby = patient_transcript_score_object.values('rna_id').annotate(tpm_n_avg=Avg('tpm_normal'),tpm_t_avg=Avg('tpm_tumor'))

    transcript_object = mtsa_rna_transcript.objects.get(id = transcript_id)
    validated_peptide = mutant_peptide_object.peptide_selection_score_id.validated_peptide_id

    tumor = mutant_peptide_object.tumor_protein
    normal = mutant_peptide_object.normal_protein
    hla = mutant_peptide_object.hla_type
    pos = mutant_peptide_object.pos
    # tumor = 'LYNTVATLY'
    #iedb
    try :
        r = requests.get(f'https://query-api.iedb.org/mhc_search?linear_sequence=eq.{tumor}&select=linear_sequence%2Cstructure_type%2Csource_organism_name%2Celution_id%2Cmhc_restriction%2Cqualitative_measure%2Chost_organism_name%2Cmhc_allele_name')
        dict_obj = json.loads(r.text)
        
    except:
        pass
    return render(request,"detail_page_mtsa.html",locals())

def detail_page_mtsa_test(request,tnh):
    try:
        th = tnh.split('_')
        th = th[0]+'_'+th[2]
        peptide = mtsa_pmhc_patient_mapping.objects.select_related('tnh').select_related('vaa_p').select_related('transcript_id').filter(tnh=tnh)
        score = scoring.objects.filter(th=th)
    except:
        pass  
    tumor = tnh.split('_')[0]
    hla = tnh.split('_')[2]
    # tumor = 'LYNTVATLY'
    try :
        r = requests.get(f'https://query-api.iedb.org/mhc_search?linear_sequence=eq.{tumor}&select=linear_sequence%2Cstructure_type%2Csource_organism_name%2Celution_id%2Cmhc_restriction%2Cqualitative_measure%2Chost_organism_name%2Cmhc_allele_name')
        dict_obj = json.loads(r.text)
        
    except:
        pass
    return render(request,"detail_page_mtsa_test.html",locals())

def detail_page_aetsa(request,id):
    source = 'aeTSA'
    mapping = aetsa_transcript_mutant_mapping.objects.get(id=id)

    mutant_peptide_id = mapping.mutant_peptide_id.id
    transcript_id = mapping.aetsa_transcript_id.id

    tumor_object = aetsa_transcript_mutant_mapping.objects.filter(mutant_peptide_id=mutant_peptide_id,aetsa_transcript_id=transcript_id)
    associated_transcript_object = aetsa_transcript_mutant_mapping.objects.filter(mutant_peptide_id=mutant_peptide_id).exclude(aetsa_transcript_id=transcript_id)
    associated_pep_object = aetsa_transcript_mutant_mapping.objects.filter(aetsa_transcript_id=transcript_id).exclude(mutant_peptide_id=mutant_peptide_id)

    
    mutant_peptide_object = mutant_peptide.objects.get(id = mutant_peptide_id)
    validated_peptide = mutant_peptide_object.peptide_selection_score_id.validated_peptide_id

    transcript_object = aetsa_transcript.objects.get(id = transcript_id)
    patient_transcript_score_object = patient_aetsa_score.objects.filter(aetsa_id = transcript_id)
    score_groupby = patient_transcript_score_object.values('aetsa_id').annotate(
        tumor_read_count_avg=Avg('tumor_read_count'),
        normal_read_count_avg=Avg('normal_read_count'),
        sum_of_tumor_and_normal_read_count_avg=Avg('sum_of_tumor_and_normal_read_count'),
        total_tumor_read_count_avg=Avg('total_tumor_read_count'),
        total_normal_read_count_avg=Avg('total_normal_read_count'),
        sum_of_total_tumor_and_normal_read_count_avg=Avg('sum_of_total_tumor_and_normal_read_count'),
        tumor_average_read_depth_avg=Avg('tumor_average_read_depth'),
        normal_average_read_depth_avg=Avg('normal_average_read_depth'),
        sum_of_expected_read_count_avg=Avg('sum_of_expected_read_count'),
        average_depth_ratio_avg=Avg('average_depth_ratio'),
        element_read_proportion_avg=Avg('element_read_proportion'),
        sum_of_element_read_count_avg=Avg('sum_of_element_read_count'))

    tumor = mutant_peptide_object.tumor_protein
    hla = mutant_peptide_object.hla_type

    #iedb
    try :
        r = requests.get(f'https://query-api.iedb.org/mhc_search?linear_sequence=eq.{tumor}&select=linear_sequence%2Cstructure_type%2Csource_organism_name%2Celution_id%2Cmhc_restriction%2Cqualitative_measure%2Chost_organism_name%2Cmhc_allele_name')
        dict_obj = json.loads(r.text)
        
    except:
        pass
   
    return render(request,"detail_page_aetsa.html",locals())

def relational_transcript(request,source,id): 

    if source =='DNA':
        associated_transcript_object = mtsa_dna_transcript_mutant_mapping.objects.filter(mutant_peptide_id=id)
    elif source =='RNA':
        associated_transcript_object = mtsa_rna_transcript_mutant_mapping.objects.filter(mutant_peptide_id=id)
    elif source =='aeTSA':
        associated_transcript_object = aetsa_transcript_mutant_mapping.objects.filter(mutant_peptide_id=id)
    
    return render(request,"relational_transcript.html",locals())

def browse_mtsa(request): 
    if request.method == 'POST' :
        request.session['tumor_protein'] = request.POST.get('tumor_protein','')
        request.session['tissue_type'] = request.POST.get('tissue_type', '')
        request.session['gene_symbol'] = request.POST.get('gene_symbol', '')
        request.session['hla_type'] = request.POST.get('hla_type','')
        request.session['ic50_min'] = request.POST.get('ic50_min',0)
        request.session['ic50_max'] = request.POST.get('ic50_max',100000)
        request.session['mut_min'] = request.POST.get('mut_min',0)
        request.session['mut_max'] = request.POST.get('mut_max',100)
    tumor_protein = request.session['tumor_protein']
    tissue_type = request.session['tissue_type']
    gene_symbol = request.session['gene_symbol']
    hla_type = request.session['hla_type']
    ic50_min = request.session['ic50_min']
    ic50_max = request.session['ic50_max']
    mut_min = request.session['mut_min']
    mut_max = request.session['mut_max']
    source = 'mTSA'
    
    # mtsa_dna_query = Q(mutant_peptide_id__tumor_protein__icontains=tumor_protein) & \
    #              Q(mutant_peptide_id__hla_type__icontains=hla_type) & \
    #              Q(tumor_type__icontains=tissue_type) & \
    #              Q(mtsa_dna_transcript_id__gene_symbol__icontains=gene_symbol)

    mtsa_rna = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_rna_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = tumor_protein,mutant_peptide_id__hla_type__icontains = hla_type, tumor_type__icontains = tissue_type,mtsa_rna_transcript_id__gene_symbol__icontains = gene_symbol,mutant_peptide_id__ic50_mut__gte = ic50_min,mutant_peptide_id__ic50_mut__lte = ic50_max,mutant_peptide_id__percent_mut__gte = mut_min,mutant_peptide_id__percent_mut__lte = mut_max)
    # mtsa_rna = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_rna_transcript_id').filter(mtsa_dna_query)
    total_count_rna = mtsa_rna.count()
    total_page_rna = int(total_count_rna/10)
    pa_rna = Paginator(mtsa_rna, per_page=10)
    page_num_rna = request.GET.get('page_rna', 1)
    try:
        page_num_rna = int(page_num_rna)
        page_object_rna = pa_rna.get_page(page_num_rna)
    except:
        page_object_rna = pa_rna.get_page(1)
    # DNA #
    mtsa_dna = mtsa_dna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_dna_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = tumor_protein,mutant_peptide_id__hla_type__icontains = hla_type, tumor_type__icontains = tissue_type,mtsa_dna_transcript_id__gene_symbol__icontains=gene_symbol,mutant_peptide_id__ic50_mut__gte = ic50_min,mutant_peptide_id__ic50_mut__lte = ic50_max,mutant_peptide_id__percent_mut__gte = mut_min,mutant_peptide_id__percent_mut__lte = mut_max )
    total_count_dna = mtsa_dna.count()
    total_page_dna = int(total_count_dna/10)
    pa_dna = Paginator(mtsa_dna, per_page=10)
    page_num_dna = request.GET.get('page_dna', 1)
    try:
        page_num_dna = int(page_num_dna)
        page_object_dna = pa_dna.get_page(page_num_dna)
    except:
        page_object_dna = pa_dna.get_page(1)

    context = {
        'mtsa_rna': mtsa_rna,
        'mtsa_dna':mtsa_dna
    }  
    return render(request,"browse_mtsa.html",locals())
#browse_mtsa_test
# def browse_mtsa_test(request): 
#     if request.method == 'POST' :
#         # tumor_protein = request.POST['tumor_protein']
#         # tissue_type = request.POST['tissue_type']
#         # source = request.POST['source']
#         # gene_symbol = request.POST['gene_symbol']
#         # hla_type = request.POST['hla_type']
#         try:    
#             request.session['tumor_protein'] = request.POST['tumor_protein']
#             request.session['tissue_type'] = request.POST['tissue_type']
#             request.session['source'] = request.POST['source']
#             request.session['gene_symbol'] = request.POST['gene_symbol']
#             request.session['hla_type'] = request.POST['hla_type'] 
#         except:
#             pass
#     tumor_protein = request.session['tumor_protein']
#     tissue_type = request.session['tissue_type']
#     source = request.session['source']
#     gene_symbol = request.session['gene_symbol']
#     hla_type = request.session['hla_type']
#     # mtsa_all = annotation_mtsa.objects.select_related('bind_mtsa_id').select_related('info_patient_id').filter(bind_mtsa_id__tumor_protein__icontains = tumor_protein,bind_mtsa_id__info_patient_id__tumor_type__icontains=tissue_type,bind_mtsa_id__info_patient_id__source__icontains=source,bind_mtsa_id__hla_type__icontains = hla_type,gene_symbol__icontains=gene_symbol )
#     mtsa_all = mtsa_pmhc_annotation_mapping.objects.select_related('tnh').select_related('transcript_id').select_related('patient').filter(tnh__tumor_protein__icontains = tumor_protein,patient__tumor_type__icontains=tissue_type,patient__source__icontains=source,tnh__hla_type__icontains = hla_type,transcript_id__gene_symbol__icontains=gene_symbol )
#     mfilter = mtsaFilter(queryset=mtsa_all)
#     if request.method == 'POST':
#         mfilter = mtsaFilter(request.POST, queryset=mtsa_all)
#     pa = Paginator(mfilter.qs, per_page=10)
#     page_num = request.GET.get('page', 1)
#     try:
#         page_num = int(page_num)
#         page_object = pa.get_page(page_num)
#     except:
#         page_object = pa.get_page(1)
#     ############ DNA##########
#     mtsa_dna_all = mtsa_dna_annotation.objects.select_related('score_id').filter(tomur_seq__icontains = tumor_protein,hla_type__icontains = hla_type,gene_symbol__icontains=gene_symbol )
#     context = {
#         'mfilter': mfilter,
#         'mtsa_dna_all':mtsa_dna_all
#     }  
#     return render(request,"browse_mtsa_test.html",locals())
def browse_aetsa(request):
    if request.method == 'POST' :
        request.session['tumor_protein'] = request.POST.get('tumor_protein','')
        request.session['tissue_type'] = request.POST.get('tissue_type', '')
        request.session['gene_symbol'] = request.POST.get('gene_symbol', '')
        request.session['hla_type'] = request.POST.get('hla_type','')
        request.session['ic50_min'] = request.POST.get('ic50_min',0)
        request.session['ic50_max'] = request.POST.get('ic50_max',100000)
        request.session['mut_min'] = request.POST.get('mut_min',0)
        request.session['mut_max'] = request.POST.get('mut_max',100)
    tumor_protein = request.session['tumor_protein']
    tissue_type = request.session['tissue_type']
    gene_symbol = request.session['gene_symbol']
    hla_type = request.session['hla_type']
    ic50_min = request.session['ic50_min']
    ic50_max = request.session['ic50_max']
    mut_min = request.session['mut_min']
    mut_max = request.session['mut_max']
    source = 'aeTSA'
    aetsa_all = aetsa_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('aetsa_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = tumor_protein,mutant_peptide_id__hla_type__icontains = hla_type, tumor_type__icontains = tissue_type,aetsa_transcript_id__gene_symbol__icontains = gene_symbol,mutant_peptide_id__ic50_mut__gte = ic50_min,mutant_peptide_id__ic50_mut__lte = ic50_max,mutant_peptide_id__percent_mut__gte = mut_min,mutant_peptide_id__percent_mut__lte = mut_max)
    total_count = aetsa_all.count()
    total_page = int(total_count/10)
    # 
    pa_aetsa = Paginator(aetsa_all, per_page=10)
    page_num_aetsa = request.GET.get('page_aetsa', 1)
    try:
        page_num_aetsa = int(page_num_aetsa)
        page_object_aetsa = pa_aetsa.get_page(page_num_aetsa)
    except:
        page_object_aetsa = pa_aetsa.get_page(1)
    return render(request,"browse_aetsa.html",locals())

def download_mTSA(request):
    file=open('/CMU_TSA/cindy2270/IEDB/mhc3_filter_everything_v3.csv','rb')  # 这个file文件句柄就是一个迭代器。 # <class '_io.TextIOWrapper'>
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="models.py"'
    return response
def download_user_filter_peptides(request):

    if request.method == 'POST' :
        request.session['tumor_protein'] = request.POST.get('tumor_protein','')
        request.session['tissue_type'] = request.POST.get('tissue_type', '')
        request.session['gene_symbol'] = request.POST.get('gene_symbol', '')
        request.session['hla_type'] = request.POST.get('hla_type','')
        request.session['source'] = request.POST.get('source')
    tumor_protein = request.session['tumor_protein']
    tissue_type = request.session['tissue_type']
    gene_symbol = request.session['gene_symbol']
    hla_type = request.session['hla_type']
    source = request.session['source']
    if source=='mTSA':
        mtsa_dna = mtsa_dna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_dna_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = tumor_protein,mutant_peptide_id__hla_type__icontains = hla_type, tumor_type__icontains = tissue_type,mtsa_dna_transcript_id__gene_symbol__icontains=gene_symbol )
        mtsa_rna = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_rna_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = tumor_protein,mutant_peptide_id__hla_type__icontains = hla_type, tumor_type__icontains = tissue_type,mtsa_rna_transcript_id__gene_symbol__icontains = gene_symbol)
        queryset = mtsa_rna.values_list('mutant_peptide_id__tumor_protein','mutant_peptide_id__hla_type','mtsa_rna_transcript_id__transcript_id','mtsa_rna_transcript_id__gene_symbol','mutant_peptide_id__ic50_mut','mutant_peptide_id__percent_mut','mutant_peptide_id__peptide_selection_score_id__stability_rank','mutant_peptide_id__peptide_selection_score_id__best_cleavage_position','mutant_peptide_id__peptide_selection_score_id__hydro_avg_score','mutant_peptide_id__peptide_selection_score_id__foreignness_score','mutant_peptide_id__peptide_selection_score_id__IEDB_anno','mutant_peptide_id__peptide_selection_score_id__dissimilarity','mutant_peptide_id__peptide_selection_score_id__validated_peptide_id')
        df = pd.DataFrame(queryset, columns=['Mutant Peptide', 'HLA Allele','Esemble Transcript ID','Gene Symbol','IC50','Percentage Mutant Rank','Stability Rank','Best Cleavage Position','Hydrophobicity','Foreignness Score','IEDB Annotation','Dissimilarity to Self','Validated'])
        df['Source From'] = 'mTSA RNA'
        queryset = mtsa_dna.values_list('mutant_peptide_id__tumor_protein','mutant_peptide_id__hla_type','mtsa_dna_transcript_id__transcript_id','mtsa_dna_transcript_id__gene_symbol','mutant_peptide_id__ic50_mut','mutant_peptide_id__percent_mut','mutant_peptide_id__peptide_selection_score_id__stability_rank','mutant_peptide_id__peptide_selection_score_id__best_cleavage_position','mutant_peptide_id__peptide_selection_score_id__hydro_avg_score','mutant_peptide_id__peptide_selection_score_id__foreignness_score','mutant_peptide_id__peptide_selection_score_id__IEDB_anno','mutant_peptide_id__peptide_selection_score_id__dissimilarity','mutant_peptide_id__peptide_selection_score_id__validated_peptide_id')
        df_d = pd.DataFrame(queryset, columns=['Mutant Peptide', 'HLA Allele','Esemble Transcript ID','Gene Symbol','IC50','Percentage Mutant Rank','Stability Rank','Best Cleavage Position','Hydrophobicity','Foreignness Score','IEDB Annotation','Dissimilarity to Self','Validated'])
        df_d['Source From'] = 'mTSA DNA'
        df = pd.concat([df,df_d])
        df['Validated'] = df['Validated'].apply(lambda x: 'Yes' if not pd.isna(x) else 'No')
    elif source=='aeTSA':
        aetsa = aetsa_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('aetsa_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = tumor_protein,mutant_peptide_id__hla_type__icontains = hla_type, tumor_type__icontains = tissue_type,aetsa_transcript_id__gene_symbol__icontains = gene_symbol)
        queryset = aetsa.values_list('mutant_peptide_id__tumor_protein','mutant_peptide_id__hla_type','aetsa_transcript_id__gene_symbol','aetsa_transcript_id__gene_element','aetsa_transcript_id__cdna_location','mutant_peptide_id__ic50_mut','mutant_peptide_id__percent_mut','mutant_peptide_id__peptide_selection_score_id__stability_rank','mutant_peptide_id__peptide_selection_score_id__best_cleavage_position','mutant_peptide_id__peptide_selection_score_id__hydro_avg_score','mutant_peptide_id__peptide_selection_score_id__foreignness_score','mutant_peptide_id__peptide_selection_score_id__IEDB_anno','mutant_peptide_id__peptide_selection_score_id__dissimilarity','mutant_peptide_id__peptide_selection_score_id__validated_peptide_id')
        df = pd.DataFrame(queryset, columns=['Mutant Peptide', 'HLA Allele','Gene Symbol','Gene Element','cDNA Location','IC50','Percentage Mutant Rank','Stability Rank','Best Cleavage Position','Hydrophobicity','Foreignness Score','IEDB Annotation','Dissimilarity to Self','Validated'])
        df['Source From'] = 'aeTSA RNA'
        df['Validated'] = df['Validated'].apply(lambda x: 'Yes' if not pd.isna(x) else 'No')
    
    # Convert queryset to DataFrame
    # df = pd.DataFrame(list(queryset.values()))
    # Set up response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="TWNeoDB.csv"'
    df.to_csv(path_or_buf=response, index=False)

    return response
def download_prioritizing_result(request,job_uuid):
    output = OUT_FILE_DIR + job_uuid
    
    file=open(output+'/final_score.csv','rb') 
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="results.csv"'
    return response

def download(request):
    return render(request,"download.html",locals())

def search_database_mTSA(request):  

    tumor_types = patient_info.objects.values_list('tumor_type', flat=True).distinct()
    
    return render(request,"search_mtsa.html",locals())

def search_database_aeTSA(request):  

    tumor_types = patient_info.objects.values_list('tumor_type', flat=True).distinct()

    return render(request,"search_aetsa.html",locals())
    
def get_page(self, number):
        """
        Return a valid page, even if the page argument isn't a number or isn't
        in range.
        """
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages
        return self.page(number)

@csrf_exempt
def upload(request):
    # ip_address=get_client_ip(request) 
    # ip_address = ip_address[0]
    
    # country = match.country
    # try:
    # country=reader.get(ip_address[0])['country']['names']['en']
    # except:
    #     country="NA"
    
    # print(country)
    mail = request.POST['email']
    
    try:
        user_id = user_info.objects.get(mail=mail).id
    except:
        ip_info = get_location()
        # print(ip_info['country'],ip_info['ip'])
        ip_address = ip_info['ip']
        country=reader.get(ip_address)['country']['names']['en']
        # print(ip_address,country)
        user_info.objects.create(
                            ip=ip_address,mail=mail,
                            country=country)
        user_id = user_info.objects.get(mail=mail).id       
    request.session['user_id'] = user_id
    

    return render(request,"upload.html",locals())

def upload_result(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        print(user_id)
        uploaded_file = request.FILES['file']
        if uploaded_file:  
            # uuid and out dir
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
            uuid_from_datetime = uuid.uuid5(uuid.NAMESPACE_DNS, formatted_datetime)
            print(uuid_from_datetime)
            job_uuid = str(uuid_from_datetime)
            user_info_instance = user_info.objects.get(pk=user_id)
            user_job.objects.create(
                uuid =job_uuid,
                user =  user_info_instance)
            output = OUT_FILE_DIR + job_uuid 
            is_output_exist = is_path_exist(output)  
            
            #read upload file
            file_content = uploaded_file.read()
            data_str = file_content.decode('utf-8')
            df = pd.read_csv(io.StringIO(data_str), sep=' ', header=None, names=['Peptide', 'HLA_Type'])
            df['Length'] = df['Peptide'].str.len()
            df.to_csv(output+ f'/{job_uuid}.csv',index=False)

            
            task_id  = async_task("app.task.all_score",job_uuid = job_uuid)

    return render(request, 'upload_result.html',locals())
               
def view_result(request,job_uuid):
    
    try:
        job = user_job.objects.get(uuid=job_uuid)
        job_status = job.status
        print(job_status)
        if job_status=='SUCCESS':
            output = OUT_FILE_DIR + job_uuid
            df_final = pd.read_csv(output+'/final_score.csv')
            df_final = df_final.fillna('')
            # df_final = df_final[['Peptide','HLA Type','Length','In TWNeoDB','IEDB Qualitative','Foreignness Anno','IC50','Percentile','Hydrophobicity','Predicted Stability','Half Life','Stability Rank','Best Cleavage Position','Best Cleavage Score','Dissimilarity','Foreignness Score','BigMHC Immunogenicity Prediction']]
        elif job_status=='WAITTING':
            df_final = []
        elif job_status=='FAILED': 
            df_final = [] 
    except user_job.DoesNotExist:
        job_status = 'NONE'
        df_final = []
        print("The job with job_uuid={} does not exist.".format(job_uuid))
    return render(request, 'view_result.html',locals())


def user_info_job(request):
    return render(request, 'user_info_job.html',locals())

def summary(request):
    # queryset = hla_in_patient.objects.all()
    # df = read_frame(queryset)
    # df_a = df.loc[df['class_type']=='A']
    # df_a = df_a.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
    # df_a = pd.read_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-a.csv')
    # fig_hla_a = px.bar(df_a, x="hla_type", y="patients", color="tumor_type", title="HLA-A type")
    # graph_html_hla_a = plot(fig_hla_a, output_type='div')

    # df_b = df.loc[df['class_type']=='B']
    # df_b = df_b.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
    # df_b = pd.read_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-b.csv')
    # fig_hla_b = px.bar(df_b, x="hla_type", y="patients", color="tumor_type", title="HLA-B type")
    # graph_html_hla_b = plot(fig_hla_b, output_type='div')

    # df_c = df.loc[df['class_type']=='C']
    # df_c = df_c.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
    # df_c = pd.read_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-c.csv')
    # fig_hla_c = px.bar(df_c, x="hla_type", y="patients", color="tumor_type", title="HLA-C type")
    # graph_html_hla_c = plot(fig_hla_c, output_type='div')


    # queryset = shared_pep_mtsa_rna.objects.all()
    # df_mtsa_rna = read_frame(queryset)
    # queryset = shared_pep_mtsa_dna.objects.all()
    # df_mtsa_dna = read_frame(queryset)
    # queryset = shared_pep_aetsa.objects.all()
    # df_aetsa = read_frame(queryset)
    # df = pd.concat([df_mtsa_rna,df_mtsa_dna,df_aetsa])
    # 使用from_records創建DataFrame
    
    # df = df.groupby(["patient_id","mutant_peptide_id","tumor_type"]).size().reset_index(name="Counts")
    # df = df.groupby(["mutant_peptide_id","tumor_type"]).size().reset_index(name="peptides shared with patients")
    # df = pd.read_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/shared_peptide.csv')
    # df = df.sort_values(by='peptides shared with patients', ascending=False)
    # df = df.loc[(df['peptides shared with patients']>2)]
    # df["TWNeo peptide"] = df["mutant_peptide_id"].apply(lambda x: "TWPEP_" + str(x))
    # fig = px.bar(df, x="TWNeo peptide",y= 'peptides shared with patients',color="tumor_type")
    # # 使用 plotly 的 plot 方法生成 HTML
    # graph_html_shared_pep = plot(fig, output_type='div')

    # queryset = patient_info.objects.values("tumor_type").annotate(count=Count('id',distinct=True))
    # df_patient_info = read_frame(queryset)
    # fig_patient = px.pie(df_patient_info, values='count', names='tumor_type')
    # graph_html_patient_info = plot(fig_patient, output_type='div')

    return render(request, 'summary.html',locals())



def send_email(request):
    # subject = 'TWNeoDB'
    # message = 'Your predicted data finished, please click this link : uuuuu'
    # from_email = 'cindy2270@gmail.com'
    # job_uuid = 'd4dfef36-f634-5f67-9ee6-57a9c47dd255'
    # user_job_instance  = user_job.objects.select_related('user').get(uuid=job_uuid)
    # recipient_list = [user_job_instance.user.mail]

    # send_mail(subject, message, from_email, recipient_list)

    return render(request, 'test1.html',locals())

def get_data(request):
    # data = mtsa_pmhc_patient_mapping.objects.select_related('tnh').select_related('vaa_p').select_related('transcript_id').all().values()
    # data = mtsa_pmhc_patient_mapping.objects.values('vaa_p__variant_position','vaa_p__patient').annotate(count=Count('vaa_p__patient',distinct=True))
    # data = mtsa_pmhc_patient_mapping.objects.annotate(count=Count('vaa_p__patient')).values('vaa_p__variant_position','count').order_by('vaa_p__variant_position')
    data = hla_in_patient.objects.values('hla_type').annotate(count=Count('id')).order_by('hla_type').order_by('-count')
    
    print(data)
    return JsonResponse({'data': list(data)})

def test1(request):
    o = open('/work1791/cindy2270/TSA_final/import_error_test.txt', 'w')

    # # 创建 Plotly 图表
    # fig = go.Figure(go.Sunburst(
    #     labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    #     parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    #     values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
    # ))

    # # 设置布局
    # fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    
    queryset = shared_pep_mtsa_rna.objects.all()
    data = list(queryset.values())
    df_mtsa_rna = pd.DataFrame.from_records(data)
    queryset = shared_pep_mtsa_dna.objects.all()
    data = list(queryset.values())
    df_mtsa_dna = pd.DataFrame.from_records(data)
    queryset = shared_pep_aetsa.objects.all()
    data = list(queryset.values())
    df_aetsa = pd.DataFrame.from_records(data)

    df = pd.concat([df_mtsa_rna,df_mtsa_dna,df_aetsa])
    # 使用from_records創建DataFrame
    
    df = df.groupby(["patient_id_id","mutant_peptide_id_id","tumor_type"]).size().reset_index(name="Counts")
    df = df.groupby(["mutant_peptide_id_id","tumor_type"]).size().reset_index(name="peptides shared with patients")
    df = df.sort_values(by='peptides shared with patients', ascending=False)
    df = df.loc[(df['peptides shared with patients']>4)]
    df["TWNeo peptide"] = df["mutant_peptide_id_id"].apply(lambda x: "TWPEP_" + str(x))
    fig = px.bar(df, x="TWNeo peptide", y="peptides shared with patients", color="tumor_type", title="Long-Form Input")
    

    # # 使用 plotly 的 plot 方法生成 HTML
    graph_html = plot(fig, output_type='div')
    o.write(f'{graph_html} \n')
    # 将图表 HTML 传递给模板
    context = {'graph_html': graph_html}
    return render(request, 'test1.html', locals())


def test(request):
    # inputtest = request.POST['annotationText']  
    # VPGEPQVVV
    annotationText = request.POST.get('annotationText', '')   
    annotationMapping = mtsa_pmhc.objects.filter(tumor_protein__icontains=annotationText).values()  
    df = pd.DataFrame(list(annotationMapping))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    # 将DataFrame写入CSV格式并将其附加到响应对象
    df.to_csv(response, index=False)
    print(df)
    # annotationTextList = annotationText.split()

    return render(request,"test.html",locals())
def test2(request):
    task_id  = async_task("app.task.test")
    print(task_id)
    task_result = result(task_id, 200)
    # print(task_result.result)
    
    return render(request,"test1.html",locals())