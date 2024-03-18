import csv
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import mtsa_pmhc,mtsa_annotation,mtsa_annotation_detail,patient,mtsa_pmhc_annotation_mapping
from app.models import mtsa_pmhc_patient_mapping,scoring
from django.db import IntegrityError
import numpy as np


class Command(BaseCommand):
    help = 'Import data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        df = pd.read_csv(csv_file)
        # df = df.where(pd.notna(df), 'Null')
        # df = df.where((df.notnull()), None)
        # df.fillna(value='None', inplace=True)
        # df = df.replace(np.nan, 'empty')
        # df.fillna(value='None', inplace=True)
        for i in range(len(df)):
            try:
                patient.objects.create(
                    id = i,
                    patient = df.at[i,'patient'],
                    sample_from='colon172', 
                    tumor_type='colon',
                    descriptopn = df.at[i,'patient'],
                    source = 'RNA',
                    TSA_type = 'mTSA'
                )
            except IntegrityError as e:
                print(e,'number:',i,'models:')
            patient_instance = patient.objects.get(patient = df.at[i,'patient'])
            
            try:
                mtsa_annotation.objects.create(
                    id = i,
                    gene_symbol = df.at[i,'gene_symbol'],
                    wildtype_protein = df.at[i,'wildtype_protein'],
                    gene_id = df.at[i,'gene_id'],
                    transcript_id = df.at[i,'transcript_id']
                )
            except IntegrityError as e:
                print(e,'number:',i,'models:')
            try:

                scoring.objects.create(
                    id = i,
                    ic50 = df.at[i,'ic50'],
                    mt  = df.at[i,'mt'],
                    th  = df.at[i,'th'],
                    best_cleavage_position	= df.at[i,'best_cleavage_position'],
                    best_cleavage_score	= df.at[i,'best_cleavage_score'],
                    predicted_stability	= df.at[i,'predicted_stability'],
                    half_life	= df.at[i,'half_life'],
                    stability_rank= df.at[i,'stability_rank'],
                    hydro_avg_score= df.at[i,'hydro_avg_score'] if not pd.isna(df.at[i, 'hydro_avg_score']) else None,
                    foreignness_score= df.at[i,'foreignness_score'] if not pd.isna(df.at[i, 'foreignness_score']) else None,
                    IEDB_anno= df.at[i,'IEDB_anno'] if not pd.isna(df.at[i, 'IEDB_anno']) else None,
                    dissimilarity= df.at[i,'dissimilarity'] if not pd.isna(df.at[i, 'dissimilarity']) else None,
                    cterm_7mer_gravy_score= df.at[i,'cterm_7mer_gravy_score'] if not pd.isna(df.at[i, 'cterm_7mer_gravy_score']) else None,
                    max_7mer_gravy_score= df.at[i,'max_7mer_gravy_score'] if not pd.isna(df.at[i, 'max_7mer_gravy_score']) else None,
                    
                )
            except IntegrityError as e:
                print(e,'number:',i,'models:')

            th_instance = scoring.objects.get(th = df.at[i,'th'])
            try:
                mtsa_pmhc.objects.create(
                    id = i,
                    tumor_protein = df.at[i,'tumor_protein'],
                    normal_protein = df.at[i,'normal_protein'],
                    length = df.at[i,'length'],
                    amino_acids_change = df.at[i,'amino_acids_change'],
                    hla_type = df.at[i,'hla_type'],
                    tnh = df.at[i,'tnh'],
                    th = th_instance
                )
            except IntegrityError as e:
                print(e,'number:',i,'models:mtsa_pmhc')
            try:

                mtsa_annotation_detail.objects.create(
                    id = i,
                    variant_position = df.at[i,'variant_position'],
                    allele_ref  = df.at[i,'allele_ref'],
                    allele_tumor = df.at[i,'allele_tumor'],
                    amino_acids_change = df.at[i,'amino_acids_change'],
                    protein_position = df.at[i,'protein_position'],
                    tpm_normal = df.at[i,'tpm_normal'],
                    tpm_tumor = df.at[i,'tpm_tumor'],
                    patient = patient_instance,
                    vaa_p = df.at[i,'vaa_p']
                )
            except IntegrityError as e:
                print(e,'number:',i,'models:mtsa_annotation_detail')
            tnh_instance = mtsa_pmhc.objects.get(tnh = df.at[i,'tnh'])
            transcript_id_instance = mtsa_annotation.objects.get(transcript_id = df.at[i,'transcript_id'])
            vaa_p_instance = mtsa_annotation_detail.objects.get(vaa_p = df.at[i,'vaa_p'])
            try:
                mtsa_pmhc_annotation_mapping.objects.create(
                    tnh = tnh_instance,
                    transcript_id = transcript_id_instance,
                    patient = patient_instance
                ) 
            except IntegrityError as e:
                print(e,'number:',i,'models:mtsa_pmhc_annotation_mapping')
            try:
                mtsa_pmhc_patient_mapping.objects.create(

                    tnh = tnh_instance,
                    transcript_id = transcript_id_instance,
                    vaa_p = vaa_p_instance
                )
            except IntegrityError as e:
                print(e,'number:',i,'models:mtsa_pmhc_patient_mapping')
        print('good')
    