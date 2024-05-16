import csv
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,validated_peptide,hla_in_patient,shared_pep_mtsa_rna
from django.db import IntegrityError
import numpy as np
from django.db.models import F
import re

class Command(BaseCommand):
    help = 'Import data from CSV file into the database'
    # python manage.py save_mtsa_rna
    # python manage.py save_mtsa_rna /work1791/cindy2270/TSA_final/colon172/final_mTSA/final_colon172_mtsa_001T.csv colon172 colon 001
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('sample_from', type=str, help='sample_from')
        parser.add_argument('tumor_type', type=str, help='tumor_type')
        parser.add_argument('patient_number', type=str, help='patient_number')

    def handle(self, *args, **options):
        o = open('/work1791/cindy2270/TSA_final/import_error.txt', 'a')
        csv_file = options['csv_file']
        sample_from = options['sample_from']
        tumor_type = options['tumor_type']
        patient_number = options['patient_number']
        df = pd.read_csv(csv_file)
        df = df.loc[~(df['gene_symbol'].str.contains('IGHC|IGHJ|IGHD|IGHV|IGKV|IGKC|IGKJ|IGLJ|IGLV|IGLC', na=False))]
        df = df.reset_index(drop=True)
        
        o.write(f'\n ======================= SAVE INFO ========================== \n')
        o.write(f' ==== {csv_file} ===== \n')
        o.write(f' ==== {sample_from} ===== \n')
        o.write(f' ==== {tumor_type} ===== \n')
        o.write(f' ==== {patient_number} ===== \n')

        o.write(f'== Total count == {len(df)} \n')
        
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
            df_hla = df.groupby(["hla_type"]).size().reset_index(name="Counts")
            o.write(f'== HLA type == \n')
            for hla in range(len(df_hla)):
                match = re.search(r'([A-Z])\*\d+:\d+', df_hla.at[hla,'hla_type'])
                hla_class = match.group(1)
                hla_in_patient.objects.create(
                    hla_type = df_hla.at[hla,'hla_type'],
                    class_type = hla_class,
                    patient_id = patient_info_instance,
                    tumor_type = tumor_type
                )
                o.write(f'{df_hla.at[hla,"hla_type"]}\n')

        except:
            patient_info_instance = patient_info.objects.get(
                sample_from	= sample_from,
                patient_number	= patient_number
            )
        
        for i in range(len(df)):
            
            try:
                mtsa_rna_transcript.objects.create(
                    gene_id = df.at[i,'gene_id'],
                    transcript_id = df.at[i,'transcript_id'],
                    gene_symbol = df.at[i,'gene_symbol'],
                    variant_position = df.at[i,'variant_position'],
                    allele_ref  = df.at[i,'allele_ref'],
                    allele_tumor = df.at[i,'allele_tumor'],
                    amino_acids_change = df.at[i,'amino_acids_change'],
                    protein_position = df.at[i,'protein_position'],
                    wildtype_protein = df.at[i,'wildtype_protein'],
                    variant_frequency = 1  
                )
                # print('1')
            except IntegrityError as e:
                # o.write(f'1___mtsa_rna_transcript___{i}___{e} \n')
                rna_id_instance = mtsa_rna_transcript.objects.get(
                    variant_position = df.at[i,'variant_position'],
                    allele_ref  = df.at[i,'allele_ref'],
                    allele_tumor = df.at[i,'allele_tumor'])
                is_patient_in = patient_transcript_score.objects.filter(rna_id = rna_id_instance,patient_id = patient_info_instance).exists()
                if not is_patient_in:
                    mtsa_rna_transcript.objects.filter(id = rna_id_instance.id).update(variant_frequency = F('variant_frequency') + 1)
                    o.write(f"\n ========== update frequency - patient : {patient_number} {df.at[i,'variant_position'] } {df.at[i,'allele_ref']} {df.at[i,'allele_tumor']} \n \n ")

            
            try:
                rna_id_instance = mtsa_rna_transcript.objects.get(
                variant_position = df.at[i,'variant_position'],
                allele_ref  = df.at[i,'allele_ref'],
                allele_tumor = df.at[i,'allele_tumor'])
                    # 因為null沒辦法判斷並constrian
                if not patient_transcript_score.objects.filter(rna_id=rna_id_instance, patient_id=patient_info_instance).exists():
                
                    patient_transcript_score.objects.update_or_create(
                        tpm_normal = df.at[i,'tpm_normal'],
                        tpm_tumor = df.at[i,'tpm_tumor'],
                        rna_id = rna_id_instance,
                        patient_id = patient_info_instance
                    )


                # print('2')
            except IntegrityError as e:
                # o.write(f'2___patient_transcript_score___{i}___{e} \n')
                pass

            validated_pep_instance = validated_peptide.objects.filter(tumor_protein=df.at[i,'tumor_protein'], hla_type=df.at[i,'hla_type'])
            if validated_pep_instance.exists():
                validated_pep_instance = validated_peptide.objects.get(tumor_protein=df.at[i,'tumor_protein'], hla_type=df.at[i,'hla_type'])

            try:
                peptide_selection_score.objects.create(
                    tumor_protein = df.at[i,'tumor_protein'],
                    hla_type = df.at[i,'hla_type'],
                    best_cleavage_position	= df.at[i,'best_cleavage_position'] if not pd.isna(df.at[i,'best_cleavage_position']) else None,
                    best_cleavage_score	= df.at[i,'best_cleavage_score'] if not pd.isna(df.at[i,'best_cleavage_score']) else None,
                    predicted_stability	= df.at[i,'predicted_stability'] ,
                    half_life	= df.at[i,'half_life'],
                    stability_rank= df.at[i,'stability_rank'],
                    hydro_avg_score= df.at[i,'hydro_avg_score'] if not pd.isna(df.at[i, 'hydro_avg_score']) else None,
                    foreignness_score= df.at[i,'foreignness_score'] if not pd.isna(df.at[i, 'foreignness_score']) else None,
                    IEDB_anno= df.at[i,'IEDB_anno'] if not pd.isna(df.at[i, 'IEDB_anno']) else None,
                    dissimilarity= df.at[i,'dissimilarity'] if not pd.isna(df.at[i, 'dissimilarity']) else None,
                    cterm_7mer_gravy_score= df.at[i,'cterm_7mer_gravy_score'] if not pd.isna(df.at[i, 'cterm_7mer_gravy_score']) else None,
                    max_7mer_gravy_score= df.at[i,'max_7mer_gravy_score'] if not pd.isna(df.at[i, 'max_7mer_gravy_score']) else None,
                    length = df.at[i,'length'],
                    validated_peptide_id = validated_pep_instance if validated_pep_instance else None
                )
                # print('3')
            except IntegrityError as e:
                # o.write(f'3___peptide_selection_score___{i}___{e} \n')
                pass


            try:
                peptide_selection_score_instance = peptide_selection_score.objects.get(
                    tumor_protein = df.at[i,'tumor_protein'],
                    hla_type = df.at[i,'hla_type']
                )
                mutant_peptide.objects.create(
                    tumor_protein = df.at[i,'tumor_protein'],
                    normal_protein = df.at[i,'normal_protein'],
                    hla_type = df.at[i,'hla_type'],
                    length = df.at[i,'length'],
                    amino_acids_change = df.at[i,'amino_acids_change'],
                    pos = df.at[i,'pos'],
                    ic50_mut = df.at[i,'ic50'],
                    percent_mut  = df.at[i,'mt'], 
                    peptide_selection_score_id = peptide_selection_score_instance
                )
                # print('4')
            except IntegrityError as e:
                # o.write(f'4___mutant_peptide___{i}___{e} \n')
                pass
            
            mtsa_rna_transcript_instance = mtsa_rna_transcript.objects.get(
                variant_position = df.at[i,'variant_position'],
                allele_ref  = df.at[i,'allele_ref'],
                allele_tumor = df.at[i,'allele_tumor'],
            )
            mutant_peptide_instance = mutant_peptide.objects.get(
                tumor_protein = df.at[i,'tumor_protein'],
                normal_protein = df.at[i,'normal_protein'],
                hla_type = df.at[i,'hla_type'],
            )
            try:
                mtsa_rna_transcript_mutant_mapping.objects.create(
                    mtsa_rna_transcript_id = mtsa_rna_transcript_instance,
                    mutant_peptide_id = mutant_peptide_instance,
                    tumor_type = tumor_type
                )
                # print('5')
            except IntegrityError as e:
                # o.write(f'5___mtsa_rna_transcript_mutant_mapping___{i}___{e} \n')
                pass
            try:
                shared_pep_mtsa_rna.objects.create(
                    patient_id = patient_info_instance,
                    rna_id = mtsa_rna_transcript_instance,
                    mutant_peptide_id = mutant_peptide_instance,
                    tumor_type = tumor_type
                )
            except IntegrityError as e:
                pass




        o.write(f' ========================== END ============================= \n')
        print('success')
        print('mTSA RNA')
        print(f' {sample_from} ')
        print(f' {tumor_type} ')
        print(f' {patient_number} ')
        print(' ')

