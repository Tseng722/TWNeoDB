import os
import glob
import subprocess
import pandas as pd
from os import path, makedirs, getcwd
import math
from django.conf import settings
import requests
import json
from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,hla_in_patient
from app.models import aetsa_transcript_mutant_mapping,patient_aetsa_score,aetsa_transcript
from app.models import shared_pep_mtsa_rna,shared_pep_mtsa_dna,shared_pep_aetsa


OUT_FILE_DIR= settings.OUTPUT_BASE_DIR

def _is_path_exist(dir, error_msg=False):
    if dir == None: return False
    elif path.exists(dir): return True
    #if error_msg: logger.error(dir+": No such file or directory\n")
    else: return False

def pvac(df,output_dir):
    if not _is_path_exist(output_dir): makedirs(output_dir)
    output_dir = path.abspath(path.expanduser(output_dir))
    for i in range(len(df)):
        hla = df.at[i,'HLA_Type']
        pep = df.at[i,'Peptide']
        l = len(pep)
        ofile = open(f'{output_dir}/{hla}_{l}.fasta','a')
        ofile.write(">" + str(pep) +'_' + hla +'_' + '\n'  + str(pep)+ '\n')
    ofile.close()
    pattern = os.path.join(output_dir, '*.fasta')
    fasta_files = glob.glob(pattern)
    final_df = pd.DataFrame()
    for file in fasta_files:
        file_name = os.path.splitext(os.path.basename(file))[0]
        hla = file_name.split('_')[0]
        mer = file_name.split('_')[1]
        try:
            cmd = f'pvacbind run  {file}  {file_name}  {hla}  NetMHCpan NetMHC  {output_dir}/{file_name}/  -e1 {mer}   -k  -t 48 -b 100000  --aggregate-inclusion-binding-threshold 100000  --net-chop-method cterm  --netmhc-stab   --iedb-install-directory /CMU_TSA/joyce7625e5/TSA_tool/data/iedb/ '   
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output = True, # Python >= 3.7 only
                text = True # Python >= 3.7 only      
            )
            o = open(f'{output_dir}/{file_name}/out.txt', 'w')
            e = open(f'{output_dir}/{file_name}/error.txt', 'w')
            o.write(result.stdout)
            e.write(result.stderr)
            o.close()
            e.close()
        
        except Exception as e:
            print(f"An exception occurred: {str(e)}")

        tmp_dir = f'{output_dir}/{file_name}/MHC_Class_I/{file_name}.filtered.tsv'
        tmp_df = pd.read_csv(tmp_dir,sep="\t")
        final_df = pd.concat([final_df,tmp_df],ignore_index=True)

    return final_df

def hydro_vector(pep):
	hydro_score={"A":1.8,"C":2.5,"D":-3.5,"E":-3.5,"F":2.8,"G":-0.4,"H":-3.2,"I":4.5,"K":-3.9,"L":3.8,"M":1.9,"N":-3.5,"P":-1.6,"Q":-3.5,"R":-4.5,"S":-0.8,"T":-0.7,"V":4.2,"W":-0.9,"Y":-1.3}
	hydrophobicity_vector=[]
	pep_list=list(pep)
	pep_len=len(pep_list)
	for pep in pep_list:
		hydrophobicity_vector.append(hydro_score[pep.upper()])
	return hydrophobicity_vector
def calculate_hydro(peptide,hla,mer,df_weight):
	f = (df_weight['HLA allele'] ==hla)
	df_tmp = df_weight.loc[f].reset_index(drop=True)
	hydro_list = hydro_vector(peptide)
	hydro_score_total = 0
	try:
		for i in range(mer): 
			hydro_score_single = (-math.log(df_tmp.iat[0,i+1],10)*hydro_list[i])
			hydro_score_total += hydro_score_single
		hydro_score_avg = hydro_score_total/mer
	except:
		hydro_score_avg = 'NA'
	return hydro_score_avg

def hydro(df):
    df_9_mer = pd.read_excel("/CMU_TSA/cindy2270/IEDB/score_TCR/abg2200_Data_file_S2.xlsx",sheet_name=0,index_col=None)
    df_8_mer = pd.read_excel("/CMU_TSA/cindy2270/IEDB/score_TCR/abg2200_Data_file_S2.xlsx",sheet_name=1,index_col=None)
    df_10_mer = pd.read_excel("/CMU_TSA/cindy2270/IEDB/score_TCR/abg2200_Data_file_S2.xlsx",sheet_name=2,index_col=None)
    df_11_mer = pd.read_excel("/CMU_TSA/cindy2270/IEDB/score_TCR/abg2200_Data_file_S2.xlsx",sheet_name=3,index_col=None)
    for i in range(len(df)):
        pep = df.at[i,'Peptide']
        hla = df.at[i,'HLA_Type']
        mer = df.at[i,'Length']
        if mer == 8:
            df_weight = df_8_mer
        elif mer == 9:
            df_weight = df_9_mer
        elif mer == 10:
            df_weight = df_10_mer
        elif mer == 11:
            df_weight = df_11_mer
        hydro_score = calculate_hydro(pep,hla,mer,df_weight)
        df.at[i,'hydro_score'] = hydro_score

    return df


def similarity(df,sample_name,output):
    container_id = "sleepy_dirac"
    r_script = "Rscript /root/local179/test_docker.R"
    output_txt = output +f'/{sample_name}.txt'
    
    dfg = df.groupby(['Peptide']).size().reset_index(name="Counts")
    dfg['Peptide'].to_csv(output_txt, header=False, index=False)

    
    command = f"docker cp {output_txt} {container_id}:/root/local179/{sample_name}.txt"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    command = f'docker start {container_id}'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    command = f'docker exec -e PATH="/root/antigen.garnish/netMHC/netMHC-4.0:/root/antigen.garnish/netMHC/netMHCII-2.3:/root/antigen.garnish/netMHC/netMHCIIpan-4.0/:/root/antigen.garnish/netMHC/netMHCpan-4.1:/root/antigen.garnish/ncbi-blast-2.10.1+-src/c++/ReleaseMT/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" -e AG_DATA_DIR="/root/antigen.garnish" {container_id} {r_script} {sample_name}'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    df_f = pd.read_table(f"/work1791/cindy2270/docker_f/f_{sample_name}.txt")
    df_d = pd.read_table(f"/work1791/cindy2270/docker_f/d_{sample_name}.txt")
    df_mf = pd.merge(dfg,df_f,how='outer',right_on='nmer',left_on='Peptide')
    df_mf.drop('nmer', axis=1, inplace=True)
    df_md = pd.merge(df_mf,df_d,how='outer',right_on='nmer',left_on='Peptide')
    df_md.drop('nmer', axis=1, inplace=True)
    

    return df_md

def is_pep_in_db(job_uuid):
    file_path = os.path.join(OUT_FILE_DIR, str(job_uuid))
    df = pd.read_csv(file_path+ f'/{job_uuid}.csv')
    df_in_db = pd.DataFrame()
    df_not_in_db = pd.DataFrame()
    db_pep = peptide_selection_score.objects.values_list('tumor_protein','hla_type')
    df_tmp = pd.DataFrame(db_pep, columns=['Mutant', 'HLA Allele'])
    df_tmp['twdb'] = df_tmp['Mutant']+'_'+df_tmp['HLA Allele']
    twdb_list = df_tmp['twdb'].tolist()
    df['th']= df['Peptide']+'_'+df['HLA_Type']
    df_in_db = df[df['th'].isin(twdb_list)]
    df_not_in_db = df[~df['th'].isin(twdb_list)]
    
    df_not_in_db.to_csv(file_path+'/not_in_db_raw.csv',index = False)
    df_in_db = df_in_db.reset_index(drop = True)
    for i in range(len(df_in_db)):

        try:
            db_pep = mutant_peptide.objects.select_related('peptide_selection_score_id').get(tumor_protein=df_in_db.at[i,'Peptide'],hla_type=df_in_db.at[i,'HLA_Type'])

            df_in_db.at[i,'IC50'] = db_pep.ic50_mut
            df_in_db.at[i,'Percentile'] = db_pep.percent_mut
            df_in_db.at[i,'Best Cleavage Position'] = db_pep.peptide_selection_score_id.best_cleavage_position
            df_in_db.at[i,'Best Cleavage Score'] = db_pep.peptide_selection_score_id.best_cleavage_score
            df_in_db.at[i,'Predicted Stability'] = db_pep.peptide_selection_score_id.predicted_stability
            df_in_db.at[i,'Half Life'] = db_pep.peptide_selection_score_id.half_life
            df_in_db.at[i,'Stability Rank'] = db_pep.peptide_selection_score_id.stability_rank
            df_in_db.at[i,'hydro_score'] = db_pep.peptide_selection_score_id.hydro_avg_score
            df_in_db.at[i,'cterm_7mer_gravy_score'] = db_pep.peptide_selection_score_id.cterm_7mer_gravy_score
            df_in_db.at[i,'max_7mer_gravy_score'] = db_pep.peptide_selection_score_id.max_7mer_gravy_score
            df_in_db.at[i,'dissimilarity'] = db_pep.peptide_selection_score_id.dissimilarity
            df_in_db.at[i,'foreignness_score'] = db_pep.peptide_selection_score_id.foreignness_score
            df_in_db.at[i,'IEDB_anno'] = db_pep.peptide_selection_score_id.IEDB_anno

        except Exception as e:
            print(f"An error occurred: {e}")
    df_in_db.to_csv(file_path+'/in_db.csv',index = False)

    return


def iedb_api(df):
    df_iedb = pd.DataFrame()
    for i in range(len(df)):
        df_tmp = pd.DataFrame()
        tumor = df.at[i,'Peptide']
        hla = df.at[i,'HLA_Type']
        print(hla)
        try:
            r = requests.get(f'https://query-api.iedb.org/mhc_search?linear_sequence=eq.{tumor}&mhc_restriction=eq.{hla}&select=linear_sequence%2Cstructure_type%2Csource_organism_name%2Celution_id%2Cmhc_restriction%2Cqualitative_measure%2Chost_organism_name%2Cmhc_allele_name')
            # r = requests.get(f'https://query-api.iedb.org/mhc_search?linear_sequence=eq.{tumor}&select=linear_sequence%2Cstructure_type%2Csource_organism_name%2Celution_id%2Cmhc_restriction%2Cqualitative_measure%2Chost_organism_name%2Cmhc_allele_name')           
            dict_obj = json.loads(r.text)
            if not dict_obj:
                df_tmp.at[0,'IEDB Qualitative'] = ''
                # df_tmp.at[0,'IEDB'] = 'nan'
                df_tmp.at[0,'Peptide'] = tumor
                df_tmp.at[0,'HLA_Type'] = hla
            else:
                pos_cpunt = 0
                neg_vount = 0
                for j,v in enumerate(dict_obj):
                    # df_tmp.at[j,'IEDB Qualitative'] = v['qualitative_measure']
                    # df_tmp.at[j,'IEDB'] =f"https://www.iedb.org/assay/{v['elution_id']}" 
                    # df_tmp.at[j,'Peptide'] = tumor
                    # df_tmp.at[j,'HLA_Type'] = hla  
                    if  'osi' in v['qualitative_measure']:
                        pos_cpunt += 1
                    elif 'ega' in v['qualitative_measure']:
                        neg_vount += 1
                df_tmp.at[0,'Peptide'] = tumor
                df_tmp.at[0,'HLA_Type'] = hla 
                df_tmp.at[0,'IEDB Qualitative'] = f'Positive : {pos_cpunt} ; Negative : {neg_vount}'
        except:
            df_tmp.at[0,'IEDB Qualitative'] = ''
            # df_tmp.at[0,'IEDB'] = 'nan'
            df_tmp.at[0,'Peptide'] = tumor
            df_tmp.at[0,'HLA_Type'] = hla
            # print(hla)
        df_iedb = pd.concat([df_iedb,df_tmp],axis = 0)
    df = pd.merge(df,df_iedb,how='outer',right_on=['Peptide','HLA_Type'],left_on=['Peptide','HLA_Type'])
    return df