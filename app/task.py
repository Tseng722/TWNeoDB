from app.score import pvac,hydro,similarity
from app.ip import get_location
from os import path, makedirs, getcwd
from django.conf import settings

from app.score import pvac,hydro,similarity,is_pep_in_db,iedb_api,bigmhc

from app.ip import get_location
from django.http import HttpResponse
import pandas as pd
from django_q.tasks import result
from app.models import user_info, user_job
from django.utils import timezone
from django.core.mail import send_mail
import os
from django.shortcuts import render, reverse

from pandas.errors import EmptyDataError 

# OUT_FILE_DIR= settings.OUTPUT_BASE_DIR
BASE_DIR = settings.BASE_DIR
OUT_FILE_DIR = os.path.join(BASE_DIR, 'tmp')
web_url = settings.WEB_URL

def is_path_exist(dir, error_msg=False):
    if dir == None: return False
    elif path.exists(dir): return True
    else: 
        makedirs(dir)
        return True

def send_email(job_uuid):
    subject = 'TWNeoDB'
    url = f'{web_url}/view_result/{job_uuid}'
    message = f'Hello,\n\nYor task for predicted data completed, please click this link :{url}  \n\nBest wishes,\nNARWHAL team'
    from_email = 'cindy2270@gmail.com'
    user_job_instance  = user_job.objects.select_related('user').get(uuid=job_uuid)
    recipient_list = [user_job_instance.user.mail]
    send_mail(subject, message, from_email, recipient_list)
    return


def all_score(job_uuid):
    is_pep_in_db(job_uuid)
    output = os.path.join(OUT_FILE_DIR, str(job_uuid))
    df = pd.read_csv(output+ f'/not_in_db_raw.csv')
    df_p = pvac(df,output) #run pvac
    df_p = df_p[['Epitope Seq','HLA Allele','Median IC50 Score','Median Percentile','cterm_7mer_gravy_score','max_7mer_gravy_score','Best Cleavage Position','Best Cleavage Score','Predicted Stability','Half Life','Stability Rank']]
    df_p.rename(columns={'Median IC50 Score': 'IC50', 'Median Percentile': 'Percentile'}, inplace=True)
    df_h = hydro(df) # hydro score

    df_s = similarity(df,job_uuid,output) # similarity score

    df_final = df_h.merge(df_p,how='right',left_on=['Peptide','HLA_Type'],right_on = ['Epitope Seq','HLA Allele'], indicator=True)
    df_final = df_final.round(3)
    df_final.drop(columns=['Epitope Seq','HLA Allele','_merge'], inplace=True)
    df_final = pd.merge(df_final,df_s,how='outer',right_on='Peptide',left_on='Peptide')
    df_final.drop(columns=['Counts'], inplace=True)

    df_in_db = pd.read_csv(output+ f'/in_db.csv')
    df_in_db['In TWNeoDB'] = 'Yes'
    df_final['In TWNeoDB'] = 'No'
    df_final = pd.concat([df_final,df_in_db],axis = 0, ignore_index=True)
    df_final.drop(columns=['th'], inplace=True)
    df_final = df_final[['Peptide','HLA_Type','In TWNeoDB','Length','IC50','Percentile','hydro_score','Predicted Stability','Half Life','Stability Rank','cterm_7mer_gravy_score','max_7mer_gravy_score','Best Cleavage Position','Best Cleavage Score','dissimilarity','foreignness_score','IEDB_anno']]
    
    df_final = iedb_api(df_final)
    file_path = os.path.join(output,'final_score.csv')   

    df_final.to_csv(file_path,index =False)
    df_bigmhc = bigmhc(file_path,output)
    df_final = pd.merge(df_final,df_bigmhc,how='outer',left_on=['Peptide','HLA_Type'],right_on = ['pep','mhc'], indicator=True)
    df_final.drop(columns=['_merge','pep','mhc'], inplace=True)
    df_final = df_final.rename(columns={'HLA_Type': 'HLA Type', 'IEDB_anno': 'Foreignness Anno','hydro_score':'Hydrophobicity','dissimilarity':'Dissimilarity','foreignness_score':'Foreignness Score','BigMHC_IM':'BigMHC Immunogenicity Prediction'})
    df_final.to_csv(file_path,index =False)

    user_job.objects.filter(uuid=job_uuid).update(status="SUCCESS",end_time = timezone.now())
    send_email(job_uuid)
    # return df_final
    return 0

def test():
    print('test')
    return 0

def check_task_status(request, task_id):
    task_result = result(task_id)
    if task_result.success:
        # Task is completed successfully
        return HttpResponse(f'Task completed! Result: {task_result.result}')
    else:
        # Task failed or is still running
        return HttpResponse('Task is still running or failed...')