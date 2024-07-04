from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,aetsa_transcript
from app.models import shared_pep_mtsa_rna,shared_pep_mtsa_dna,shared_pep_aetsa,hla_in_patient,aetsa_transcript_mutant_mapping,user_info,user_job
from django.forms.models import model_to_dict
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db import connection
import pandas as pd
from django_pandas.io import read_frame
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
from django.conf import settings
import os
BASE_DIR = settings.BASE_DIR
OUT_HTML_DIR = os.path.join(BASE_DIR, 'templates')
class Command(BaseCommand):
    help = 'test'

    # def add_arguments(self, parser):
    # python manage.py test

    def handle(self, *args, **options):
        # count_result = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_rna_transcript_id').select_related('patient_transcript_score_r').filter(mtsa_rna_transcript_id__variant_frequency = 2 ).count()
        # count_result = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_rna_transcript_id').filter(mutant_peptide_id__peptide_selection_score_id = 38775 )
        
        #-------------
        # tumor_protein = ''
        # hla_type = 'A'
        # tissue_type = 'colon'
        # gene_symbol = 'USP2'
        # mtsa_rna = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_rna_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = tumor_protein,mutant_peptide_id__hla_type__icontains = hla_type, mtsa_rna_transcript_id__patient_transcript_score_r__patient_id__tumor_type__icontains = tissue_type, mtsa_rna_transcript_id__gene_symbol__icontains = gene_symbol )
        # patient = patient_transcript_score.objects..all()
        #-------------
        # mtsa_rna = mtsa_rna_transcript_mutant_mapping.objects.filter()
        #-------------
        #反向搜索
        # mtsa_rna_ids = mtsa_rna_transcript.objects.filter(variant_frequency=2).values_list('id', flat=True)
        # related_data = patient_transcript_score.objects.filter(rna_id__in=mtsa_rna_ids)

        # rna_ids = mtsa_rna_transcript_mutant_mapping.objects.filter(mutant_peptide_id=49439).values_list('mtsa_rna_transcript_id', flat=True)
        # patientTranscriptScore = patient_transcript_score.objects.filter(rna_id__in=rna_ids)
        

        # for item in patientTranscriptScore:
        #     print(item.rna_id.gene_id)

        #-------------
        # mutant_peptide_id = 49439
        # mutant_peptide_object = mutant_peptide.objects.get(id = mutant_peptide_id)
        # print(mutant_peptide_object.tumor_protein)
        
        
        #-------------
        # tumor_test = 'FPSSTTMPGV'
        # mutant_peptide_object = mutant_peptide.objects.get(tumor_protein = tumor_test,hla_type = 'HLA-A*02:03')
        # rna_ids_list = mtsa_rna_transcript_mutant_mapping.objects.filter(mutant_peptide_id__tumor_protein = tumor_test,mutant_peptide_id__hla_type = 'HLA-A*02:03').values_list('mtsa_rna_transcript_id', flat=True)
        # print(rna_ids_list)
        
        # patient_transcript_score_object = patient_transcript_score.objects.filter(rna_id__in=rna_ids_list)
        # print(patient_transcript_score_object)
        # for i in patient_transcript_score_object:
        #     print(i.id, i.rna_id, i.dna_id, i.patient_id)

        # rna_id_instance = mtsa_rna_transcript.objects.get(
        #             variant_position = 'chr7:100995340',
        #             allele_ref  = 'G',
        #             allele_tumor = 'A')
        # print(rna_id_instance)
        # patient_transcript_score_object = patient_transcript_score.objects.filter(rna_id = 55363)
      
        
        #-------------

        # count_result = mtsa_rna_transcript.objects.filter(variant_position ='chr10:103049719').count()

        # for i in count_result:

        # print(f"符合条件的记录数量为: {count_result}")
        # print(result)
        # for instance in count_result:
            # model_dict = model_to_dict(instance)
            # print(instance.mtsa_rna_transcript)

        # print(count_result.mutant_peptide_id__peptide_selection_score_id.predicted_stability)

        # patient_instance = patient.objects.get(patient = 'colon172_mtsa_022T')
        # print(patient_instance.source)

        # ====================
        # tumor_type_counts = patient_info.objects.values('tumor_type').annotate(count=Count('id')).order_by('-count')
        # total_tumor_count = tumor_type_counts.count()
        # total_patient_count = patient_info.objects.count()
        # =====================
        # t = aetsa_transcript.objects.filter(id=1).values_list('id', flat=True)
        # print(t)
        # =====================
        # 驗證
        # a = peptide_selection_score.objects.filter(hla_type = 'HLA-A*11:01',validated_peptide_id__isnull=False)
        # for i in a :
        #     print(i.tumor_protein)

        # ======================
        # object turn to df

        # 獲取所有對象
        # queryset = shared_pep_mtsa_rna.objects.select_related('patient_id').all()

        # 將queryset轉換為字典列表
        # data = list(queryset.values())

        # 使用from_records創建DataFrame

        # df = pd.DataFrame.from_records(data)
        # df = read_frame(queryset)
        # df = df.loc[df['class_type']=='A']
        # df = df.groupby(["hla_type"]).size().reset_index(name="counts")

        
        # print(df)
        # =================
        # patient_info

        # o = patient_info.objects.filter(sample_from='oral103')
        # print(o.count())
        # =================
        # download test
        # tumor_protein = 'YFWTS'
        # tissue_type = 'colon'
        # gene_symbol = ''
        # hla_type = ''
        # mtsa_rna = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_rna_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = tumor_protein,mutant_peptide_id__hla_type__icontains = hla_type, tumor_type__icontains = tissue_type,mtsa_rna_transcript_id__gene_symbol__icontains = gene_symbol)
        # # print(list(mtsa_rna.values()))
        # print(mtsa_rna.values_list('mutant_peptide_id__tumor_protein','mutant_peptide_id__hla_type'))
        # queryset = mtsa_rna.values_list('mutant_peptide_id__tumor_protein','mutant_peptide_id__hla_type')
        # df = pd.DataFrame(queryset, columns=['Mutant', 'HLA Allele'])

        # # 打印 DataFrame
        # print(df)
        # ==============================
        # user upload 
        # db_pep = peptide_selection_score.objects.values_list('tumor_protein','hla_type')
        # df = pd.DataFrame(db_pep, columns=['Mutant', 'HLA Allele'])
        # df['twdb'] = df['Mutant']+'_'+df['HLA Allele']
        # twdb_list = df['twdb'].tolist()
        # data = [
        #     ('GLSSRAVAL', 'HLA-A*02:01'),
        #     ('LLAHVHYTV', 'HLA-A*02:01'),
        #     ('YSDLHAFYY', 'HLA-A*01:01'),
        #     ('FSDYYDLSY', 'HLA-A*01:01'),
        #     ('LYNTVATLY', 'HLA-A*02:03'),
        #     ('TLFLQMNSL', 'HLA-A*02:01')
        # ]

        # df = pd.DataFrame(data, columns=['Peptide', 'HLA_Type'])
        # print(df)
        # for i in range(len(df)):
        #     try:
        #         db_pep = mutant_peptide.objects.select_related('peptide_selection_score_id').get(tumor_protein=df.at[i,'Peptide'],hla_type=df.at[i,'HLA_Type'])
        #         print(db_pep.peptide_selection_score_id.tumor_protein)
        #         print(db_pep.peptide_selection_score_id.cterm_7mer_gravy_score)
        #     except Exception as e:
        #         print(f"An error occurred: {e}")

        # ==================
        # 儲存summary html
        # df_a = pd.read_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-a.csv')
        # fig_hla_a = px.bar(df_a, x="hla_type", y="patients", color="tumor_type", title="HLA-A type")
        # graph_html_hla_a = plot(fig_hla_a, output_type='div')
        # with open('/work1791/cindy2270/web/web_v1/webV1/templates/graph_hla_a.html', 'w') as file:
        #     file.write(graph_html_hla_a)

        # queryset = patient_info.objects.values("tumor_type").annotate(count=Count('id',distinct=True))
        # df_patient_info = read_frame(queryset)
        # fig_patient = px.pie(df_patient_info, values='count', names='tumor_type')
        # graph_html_patient_info = plot(fig_patient, output_type='div')
        # with open(OUT_HTML_DIR+'/graph_patient_info.html', 'w') as file:
        #     file.write(graph_html_patient_info)

        #=============================
        ## mutant_pep = mutant_peptide.
        # data = shared_pep_mtsa_rna.objects.select_related('mutant_peptide_id').values("patient_id","mutant_peptide_id__tumor_protein","tumor_type").distinct()
        # mtsa_rna = data.values("mutant_peptide_id__tumor_protein","tumor_type").annotate(count=Count('patient_id',distinct=True))
        # df_mtsa_rna = read_frame(mtsa_rna.filter(count__gt=1))
        # print(df_mtsa_rna)
        #=============================
        #ig gene
        # data = mtsa_rna_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('mtsa_rna_transcript_id').values("mutant_peptide_id__tumor_protein","mtsa_rna_transcript_id__gene_symbol").filter(mtsa_rna_transcript_id__gene_symbol__icontains='IGKV')
        # df = read_frame(data)
        # df2 = df.groupby(["mutant_peptide_id__tumor_protein","mtsa_rna_transcript_id__gene_symbol"]).size().reset_index(name="Counts")
        # print(len(df))
        # print(df)

        # ===========================
        # aetsa_all = aetsa_transcript_mutant_mapping.objects.select_related('mutant_peptide_id').select_related('aetsa_transcript_id').filter(mutant_peptide_id__tumor_protein__icontains = 'HHARLILYF',mutant_peptide_id__hla_type__icontains = 'HLA-A*24:02', aetsa_transcript_id__gene_symbol__icontains = 'nan')
        # for i in aetsa_all :
        #     print(i.aetsa_transcript_id.gene_symbol)

        # ======================  計算病人數量
        # dna_patient = shared_pep_mtsa_rna.objects.values('tumor_type','patient_id').annotate(count=Count('patient_id'))
        # df = read_frame(dna_patient)
        # print(df)

        # =========================   刪除table
        # user_job.objects.all().delete()
        user_job_ins = user_job.objects.filter(status='SUCCESS')
        for i in user_job_ins:
            print(i.pep_count,str(i.end_time-i.start_time).split('.')[0])
            
        

        

        # 打印结果
        # print(tumor_type_counts)
        # print(total_patient_count)
        # print(f'Total tumor types: {total_tumor_count}')

