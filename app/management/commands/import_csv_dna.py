import csv
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import mtsa_dna_annotation,mtsa_dna_score
from django.db import IntegrityError
import numpy as np


class Command(BaseCommand):
    help = 'Import data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        o = open('/work1791/cindy2270/TSA_final/import_error.txt', 'a')
        csv_file = options['csv_file']

        df = pd.read_csv(csv_file)
        # df = df.where(pd.notna(df), 'Null')
        # df = df.where((df.notnull()), None)
        # df.fillna(value='None', inplace=True)
        # df = df.replace(np.nan, 'empty')
        # df.fillna(value='None', inplace=True)
        for i in range(len(df)):
            
            try:
                mtsa_dna_score.objects.create(
                    hla_type = df.at[i,'HLA Allele'],
                    tomur_seq = df.at[i,'MT Epitope Seq'],
                    predicted_stability = df.at[i,'Predicted Stability'],
                    half_life = df.at[i,'Half Life'],
                    stability_rank = df.at[i,'Stability Rank'],
                    length = df.at[i,'Peptide Length']
                )
            except IntegrityError as e:
                o.write(f'0___mtsa_dna_score___{e}___{i} \n')
                
            
            try:
                score_instance = mtsa_dna_score.objects.get(tomur_seq = df.at[i,'MT Epitope Seq'],hla_type = df.at[i,'HLA Allele'])

                mtsa_dna_annotation.objects.create(
                    transcript_id = df.at[i,'Transcript'],
                    gene_symbol = df.at[i,'Gene Symbol'],
                    gene_id = df.at[i,'Ensembl Gene ID'],
                    variant_type = df.at[i,'Variant Type'],
                    mutation = df.at[i,'Mutation'],
                    protein_position = df.at[i,'Protein Position'],
                    ic50_mut = df.at[i,'IC50 MT'],
                    ic50_wild = df.at[i,'IC50 WT'],
                    percent_mut = df.at[i,'%ile MT'],
                    percent_wild = df.at[i,'%ile WT'],
                    chromosome = df.at[i,'Chromosome'],
                    start = df.at[i,'Start'],
                    stop = df.at[i,'Stop'],
                    reference = df.at[i,'Reference'],
                    variant = df.at[i,'Variant'],
                    pos = df.at[i,'Pos'],
                    hla_type = df.at[i,'HLA Allele'],
                    tomur_seq = df.at[i,'MT Epitope Seq'],
                    normal_seq = df.at[i,'WT Epitope Seq'],
                    score_id = score_instance

                )
            except IntegrityError as e:
                o.write(f'1___mtsa_dna_annotation___{i}___{e} \n')

            
            
        print('good')
    