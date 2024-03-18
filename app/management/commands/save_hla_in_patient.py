import csv
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import patient_info,hla_in_patient
from django.db import IntegrityError
import numpy as np
from django.db.models import F

class Command(BaseCommand):
    help = 'Import data from CSV file into the database'
    # python manage.py save_hla_in_patient

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('sample_from', type=str, help='sample_from')
        
    def handle(self, *args, **options):
        o = open('/work1791/cindy2270/TSA_final/import_error_hla.txt', 'w')
        csv_file = options['csv_file']
        sample_from = options['sample_from']
        df = pd.read_csv(csv_file)
        o.write(f'==Total== {len(df)} \n')

        for i in range(len(df)):
            patient_number = df.at[i,'patient number']
            # patient_info_instance = patient_info.objects.get(
            #     sample_from	= sample_from,
            #     patient_number	= patient_number
            # )
            hla_in_patient.objects.create(
                    hla_type = df.at[i,'HLA'],
                    class_type = df.at[i,'type'],
                    patient_number = df.at[i,'patient number'],
                    
                )





