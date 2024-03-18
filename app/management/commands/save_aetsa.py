import csv
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import patient_info,peptide_selection_score,mutant_peptide,aetsa_transcript_mutant_mapping,patient_aetsa_score,aetsa_transcript,validated_peptide,shared_pep_aetsa
from django.db import IntegrityError
import numpy as np
from django.db.models import F
import MySQLdb
import re


class Command(BaseCommand):
    help = 'Import data from CSV file into the database'
    # python manage.py save_aetsa /work1791/cindy2270/TSA_final/colon172/final_aeTSA/final_aetsa_colon172_018.csv colon172 colon 018

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('sample_from', type=str, help='sample_from')
        parser.add_argument('tumor_type', type=str, help='tumor_type')
        parser.add_argument('patient_number', type=str, help='patient_number')

    def handle(self, *args, **options):
        o = open('/work1791/cindy2270/TSA_final/import_error.txt', 'w')
        csv_file = options['csv_file']
        sample_from = options['sample_from']
        tumor_type = options['tumor_type']
        patient_number = options['patient_number']
        df = pd.read_csv(csv_file)
        o.write(f'\n ======================= SAVE INFO ========================== \n')
        o.write(f' ==== {csv_file} ===== \n')
        o.write(f' ==== {sample_from} ===== \n')
        o.write(f' ==== {tumor_type} ===== \n')
        o.write(f' ==== {patient_number} ===== \n')
        o.write(f'==Total== {len(df)} \n')
        try:
            patient_info.objects.create(
                sample_from	= sample_from,
                tumor_type	= tumor_type,
                patient_number	= patient_number,
                source = 'RNA'
            )
            patient_info_instance = patient_info.objects.get(
                sample_from	= sample_from,
                patient_number	= patient_number
            )
        except IntegrityError as e:
            patient_info_instance = patient_info.objects.get(
                sample_from	= sample_from,
                patient_number	= patient_number
            )
        for i in range(len(df)):
            try:
                aetsa_transcript.objects.create(
                    gene_id = df.at[i,'gene_id'],
                    translated_tumor_peptide = df.at[i,'Translated tumor peptide'],
                    gene_symbol = df.at[i,'gene_symbol'],
                    gene_element = df.at[i,'Gene element'],
                    cdna_location  = df.at[i,'cDNA location'],
                    cdna_sequence  = df.at[i,'cDNA sequence'],
                    putative_neoantigen_type  = df.at[i,'Putative neoantigen type']
                )
            except IntegrityError as e:
                pass
            aetsa_id_instance = aetsa_transcript.objects.get(
                    translated_tumor_peptide = df.at[i,'Translated tumor peptide'],
                    cdna_location  = df.at[i,'cDNA location'],
                    gene_element = df.at[i,'Gene element'],
                )
            try:
                patient_aetsa_score.objects.create(
                    tumor_read_count = df.at[i,'Tumor read count'],
                    normal_read_count = df.at[i,'Normal read count'],
                    sum_of_tumor_and_normal_read_count  = df.at[i,'Sum of tumor and normal read count'],
                    sum_of_total_tumor_and_normal_read_count = df.at[i,'Sum of total tumor and normal read count'],
                    total_normal_read_count =  df.at[i,'Total normal read count'],
                    total_tumor_read_count =  df.at[i,'Total tumor read count'],
                    tumor_average_read_depth =  df.at[i,'Tumor average read depth'],
                    normal_average_read_depth =  df.at[i,'Normal average read depth'],
                    sum_of_expected_read_count =  df.at[i,'Sum of expected read count'],
                    average_depth_ratio =  float(df.at[i,'Average depth ratio']) if df.at[i, 'Average depth ratio'] != np.inf else float('1.79e308'),
                    element_read_proportion =  df.at[i,'Element read proportion (%)'],
                    sum_of_element_read_count =  df.at[i,'Sum of element read count'],
                    aetsa_id = aetsa_id_instance,
                    patient_id = patient_info_instance
		
                )
            except IntegrityError as e:
                pass
            except MySQLdb.err.ProgrammingError as e:
                if df.at[i, 'Average depth ratio']== np.inf:
                    print(i,df.at[i, 'Average depth ratio'],df.at[i,'Element read proportion (%)'])
            
            validated_pep_instance = validated_peptide.objects.filter(tumor_protein=df.at[i,'tumor_protein'], hla_type=df.at[i,'HLA Allele'])
            if validated_pep_instance.exists():
                validated_pep_instance = validated_peptide.objects.get(tumor_protein=df.at[i,'tumor_protein'], hla_type=df.at[i,'HLA Allele'])

            try:
                peptide_selection_score.objects.create(
                    tumor_protein = df.at[i,'tumor_protein'],
                    hla_type = df.at[i,'HLA Allele'],
                    best_cleavage_position	= df.at[i,'Best Cleavage Position'] if not pd.isna(df.at[i,'Best Cleavage Position']) else None,
                    best_cleavage_score	= df.at[i,'Best Cleavage Score'] if not pd.isna(df.at[i,'Best Cleavage Score']) else None,
                    predicted_stability	= df.at[i,'Predicted Stability'],
                    half_life	= df.at[i,'Half Life'],
                    stability_rank= df.at[i,'Stability Rank'],
                    hydro_avg_score= df.at[i,'hydro_avg_score'] if not pd.isna(df.at[i, 'hydro_avg_score']) else None,
                    foreignness_score= df.at[i,'foreignness_score'] if not pd.isna(df.at[i, 'foreignness_score']) else None,
                    IEDB_anno= df.at[i,'IEDB_anno'] if not pd.isna(df.at[i, 'IEDB_anno']) else None,
                    dissimilarity= df.at[i,'dissimilarity'] if not pd.isna(df.at[i, 'dissimilarity']) else None,
                    cterm_7mer_gravy_score= df.at[i,'cterm_7mer_gravy_score'] if not pd.isna(df.at[i, 'cterm_7mer_gravy_score']) else None,
                    max_7mer_gravy_score= df.at[i,'max_7mer_gravy_score'] if not pd.isna(df.at[i, 'max_7mer_gravy_score']) else None,
                    length = df.at[i,'length'],
                    validated_peptide_id = validated_pep_instance if validated_pep_instance else None
                )
            except IntegrityError as e:
                pass
            peptide_selection_score_instance = peptide_selection_score.objects.get(
                    tumor_protein = df.at[i,'tumor_protein'],
                    hla_type = df.at[i,'HLA Allele']
                )
            try:
                mutant_peptide.objects.create(
                    tumor_protein = df.at[i,'tumor_protein'],
                    normal_protein = 'NA',
                    hla_type = df.at[i,'HLA Allele'],
                    length = df.at[i,'length'],
                    ic50_mut = df.at[i,'IC50 MT'],
                    percent_mut  = df.at[i,'%ile MT'], 
                    peptide_selection_score_id = peptide_selection_score_instance
                )
            except IntegrityError as e:
                pass

            mutant_peptide_instance = mutant_peptide.objects.get(
                    tumor_protein = df.at[i,'tumor_protein'],
                    normal_protein = 'NA',
                    hla_type = df.at[i,'HLA Allele']
                )
            try:
                aetsa_transcript_mutant_mapping.objects.create(
                    aetsa_transcript_id = aetsa_id_instance,
                    mutant_peptide_id = mutant_peptide_instance,
                    tumor_type = tumor_type
                )
            except IntegrityError as e:
                pass
            try:
                shared_pep_aetsa.objects.create(
                    patient_id = patient_info_instance,
                    aetsa_id = aetsa_id_instance,
                    mutant_peptide_id = mutant_peptide_instance,
                    tumor_type = tumor_type
                )
            except IntegrityError as e:
                pass

        o.write(f' ========================== END ============================= \n')
        print('success')
        print(f' {sample_from} ')
        print(f' {tumor_type} ')
        print(f' {patient_number} ')
        print(' ')



