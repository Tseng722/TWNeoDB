import csv
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,validated_peptide,shared_pep_mtsa_dna,hla_in_patient
from django.db import IntegrityError
import numpy as np
from django.db.models import F
import re

class Command(BaseCommand):
    help = 'Import data from CSV file into the database'
    # python manage.py save_mtsa_dna_with_rna /work1791/cindy2270/TSA_final/oral103/final/final_mtsa_DNA_oral103_004.csv oral103 oral 004
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
        df = df.dropna(subset=['WT Epitope Seq'])
        df = df.reset_index(drop = True)
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
                source = 'DNA'
            )
            patient_info_instance = patient_info.objects.get(
                sample_from	= sample_from,
                patient_number	= patient_number
            )
            df_hla = df.groupby(["HLA Allele"]).size().reset_index(name="Counts")
            o.write(f'== HLA type == \n')
            for hla in range(len(df_hla)):
                match = re.search(r'([A-Z])\*\d+:\d+', df_hla.at[hla,'HLA Allele'])
                hla_class = match.group(1)
                hla_in_patient.objects.create(
                    hla_type = df_hla.at[hla,'HLA Allele'],
                    class_type = hla_class,
                    patient_id = patient_info_instance,
                    tumor_type = tumor_type
                )
                o.write(f'{df_hla.at[hla,"HLA Allele"]}\n')
        except:
            patient_info_instance = patient_info.objects.get(
                sample_from	= sample_from,
                patient_number	= patient_number
            )
        

        for i in range(len(df)):
            try:
                mtsa_dna_transcript.objects.create(
                    gene_id = df.at[i,'Ensembl Gene ID'],
                    transcript_id = df.at[i,'Transcript'],
                    gene_symbol = df.at[i,'Gene Symbol'],
                    chromosome = df.at[i,'Chromosome'],
                    start = df.at[i,'Start'],
                    stop = df.at[i,'Stop'],
                    reference = df.at[i,'Reference'],
                    variant = df.at[i,'Variant'],
                    mutation = df.at[i,'Mutation'],
                    protein_position = df.at[i,'Protein Position'],
                    variant_type = df.at[i,'Variant Type'],
                    variant_frequency = 1  
                )
            except IntegrityError as e:
                dna_id_instance = mtsa_dna_transcript.objects.get(
                    chromosome = df.at[i,'Chromosome'],
                    start = df.at[i,'Start'],
                    stop = df.at[i,'Stop']
                )
                is_patient_in = patient_transcript_score.objects.filter(dna_id = dna_id_instance,patient_id = patient_info_instance).exists()
                if not is_patient_in:
                    mtsa_dna_transcript.objects.filter(id = dna_id_instance.id).update(variant_frequency = F('variant_frequency') + 1)
                    o.write(f"\n ========== update frequency - patient : {patient_number} {df.at[i,'Chromosome'] } {df.at[i,'Start']} {df.at[i,'Stop']} \n \n ")
            try:
                dna_id_instance = mtsa_dna_transcript.objects.get(
                    chromosome = df.at[i,'Chromosome'],
                    start = df.at[i,'Start'],
                    stop = df.at[i,'Stop']
                )
                if not patient_transcript_score.objects.filter(dna_id = dna_id_instance,patient_id = patient_info_instance).exists():
                    patient_transcript_score.objects.create(
                        fold_change = df.at[i,'Median Fold Change'],
                        tumor_dna_depth = df.at[i,'Tumor DNA Depth'],
                        tumor_dna_vaf = df.at[i,'Tumor DNA VAF'],
                        dna_id = dna_id_instance,
                        patient_id = patient_info_instance
                    )
            except IntegrityError as e:
                # o.write(f'2___patient_transcript_score___{i}___{e} \n')
                pass
            validated_pep_instance = validated_peptide.objects.filter(tumor_protein=df.at[i,'MT Epitope Seq'], hla_type=df.at[i,'HLA Allele'])
            if validated_pep_instance.exists():
                validated_pep_instance = validated_peptide.objects.get(tumor_protein=df.at[i,'MT Epitope Seq'], hla_type=df.at[i,'HLA Allele'])

            
            try:
                peptide_selection_score.objects.create(
                    tumor_protein = df.at[i,'MT Epitope Seq'],
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
                    length = df.at[i,'Peptide Length'],
                    validated_peptide_id = validated_pep_instance if validated_pep_instance.exists() else None
                )
                # print('3')
            except IntegrityError as e:
                # o.write(f'3___peptide_selection_score___{i}___{e} \n')
                pass
            try:
                peptide_selection_score_instance = peptide_selection_score.objects.get(
                    tumor_protein = df.at[i,'MT Epitope Seq'],
                    hla_type = df.at[i,'HLA Allele']
                )
                mutant_peptide.objects.create(
                    tumor_protein = df.at[i,'MT Epitope Seq'],
                    normal_protein = df.at[i,'WT Epitope Seq'],
                    hla_type = df.at[i,'HLA Allele'],
                    length = df.at[i,'Peptide Length'],
                    amino_acids_change = df.at[i,'Mutation'],
                    pos = df.at[i,'Pos'],
                    ic50_mut = df.at[i,'IC50 MT'],
                    percent_mut  = df.at[i,'%ile MT'],
                    ic50_wild = df.at[i,'IC50 WT'] if not pd.isna(df.at[i,'IC50 WT']) else None,
                    percent_wild  = df.at[i,'%ile WT'] if not pd.isna(df.at[i,'%ile WT']) else None,
                    peptide_selection_score_id = peptide_selection_score_instance
                )
                # print('4')
            except IntegrityError as e:
                # o.write(f'4___mutant_peptide___{i}___{e} \n')
                pass
            mtsa_dna_transcript_instance = mtsa_dna_transcript.objects.get(
                    chromosome = df.at[i,'Chromosome'],
                    start = df.at[i,'Start'],
                    stop = df.at[i,'Stop']
                )
            mutant_peptide_instance = mutant_peptide.objects.get(
                tumor_protein = df.at[i,'MT Epitope Seq'],
                normal_protein = df.at[i,'WT Epitope Seq'],
                hla_type = df.at[i,'HLA Allele'],
            )
            try:
                mtsa_dna_transcript_mutant_mapping.objects.create(
                    mtsa_dna_transcript_id = mtsa_dna_transcript_instance,
                    mutant_peptide_id = mutant_peptide_instance,
                    tumor_type = tumor_type
                )
                # print('5')
            except IntegrityError as e:
                # o.write(f'5___mtsa_rna_transcript_mutant_mapping___{i}___{e} \n')
                pass
            try:
                shared_pep_mtsa_dna.objects.create(
                    patient_id = patient_info_instance,
                    dna_id = mtsa_dna_transcript_instance,
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




