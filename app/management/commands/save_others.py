import csv
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import validated_peptide
from django.db import IntegrityError
import numpy as np

class Command(BaseCommand):
    help = 'test'

    # python manage.py save_others

    def handle(self, *args, **options):
        df = pd.read_csv('/CMU_TSA/cindy2270/external/final/final_all_valdiated_tcr_v1.csv',engine='python')
        for i in range(len(df)):
            validated_peptide.objects.create(
                tumor_protein = df.at[i,'Mutant'],
                hla_type = df.at[i,'Allele'],
                tcr = df.at[i,'immuno'],
                deepneo = df.at[i,'deep'] if not pd.isna(df.at[i, 'deep']) else None,
                iedb_tcr = df.at[i,'iedb'] if not pd.isna(df.at[i, 'iedb']) else None,
                prime = df.at[i,'prime'] if not pd.isna(df.at[i, 'prime']) else None,
                best_cleavage_position	= df.at[i,'Best Cleavage Position'] if not pd.isna(df.at[i, 'Best Cleavage Position']) else None,
                best_cleavage_score	= df.at[i,'Best Cleavage Score'] if not pd.isna(df.at[i, 'Best Cleavage Score']) else None,
                predicted_stability	= df.at[i,'Predicted Stability'] if not pd.isna(df.at[i, 'Predicted Stability']) else None,
                half_life	= df.at[i,'Half Life'] if not pd.isna(df.at[i, 'Half Life']) else None,
                stability_rank= df.at[i,'Stability Rank'] if not pd.isna(df.at[i, 'Stability Rank']) else None,
                hydro_avg_score= df.at[i,'hydro_avg_score'] if not pd.isna(df.at[i, 'hydro_avg_score']) else None,
                foreignness_score= df.at[i,'foreignness_score'] if not pd.isna(df.at[i, 'foreignness_score']) else None,
                IEDB_anno= df.at[i,'IEDB_anno'] if not pd.isna(df.at[i, 'IEDB_anno']) else None,
                dissimilarity= df.at[i,'dissimilarity'] if not pd.isna(df.at[i, 'dissimilarity']) else None,
                cterm_7mer_gravy_score= df.at[i,'cterm_7mer_gravy_score'] if not pd.isna(df.at[i, 'cterm_7mer_gravy_score']) else None,
                max_7mer_gravy_score= df.at[i,'max_7mer_gravy_score'] if not pd.isna(df.at[i, 'max_7mer_gravy_score']) else None,
                length = df.at[i,'length']
            )
            