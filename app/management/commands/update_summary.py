from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,aetsa_transcript
from app.models import shared_pep_mtsa_rna,shared_pep_mtsa_dna,shared_pep_aetsa,hla_in_patient
from django.forms.models import model_to_dict
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db import connection
import pandas as pd
from django_pandas.io import read_frame
class Command(BaseCommand):
    help = 'update_summary'

    # def add_arguments(self, parser):
    # python manage.py update_summary

    def handle(self, *args, **options):
        queryset = hla_in_patient.objects.all()
        df = read_frame(queryset)
        df_a = df.loc[df['class_type']=='A']
        df_a = df_a.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        df_a.to_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-a.csv',index = False)
        

        df_b = df.loc[df['class_type']=='B']
        df_b = df_b.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        df_b.to_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-b.csv',index = False)
        

        df_c = df.loc[df['class_type']=='C']
        df_c = df_c.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        df_c.to_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-c.csv',index = False)


        data = shared_pep_mtsa_rna.objects.values("patient_id","mutant_peptide_id","tumor_type").distinct()
        mtsa_rna = data.values("mutant_peptide_id","tumor_type").annotate(count=Count('patient_id',distinct=True))
        df_mtsa_rna = read_frame(mtsa_rna.filter(count__gt=1))
        df_mtsa_rna['tsa type'] = 'mTSA(RNA)'
        data = shared_pep_mtsa_dna.objects.values("patient_id","mutant_peptide_id","tumor_type").distinct()
        mtsa_dna = data.values("mutant_peptide_id","tumor_type").annotate(count=Count('patient_id',distinct=True))
        df_mtsa_dna = read_frame(mtsa_dna.filter(count__gt=1))
        df_mtsa_dna['tsa type'] = 'mTSA(DNA)'

        data = shared_pep_aetsa.objects.values("patient_id","mutant_peptide_id","tumor_type").distinct()
        aetsa = data.values("mutant_peptide_id","tumor_type").annotate(count=Count('patient_id',distinct=True))
        df_aetsa = read_frame(aetsa.filter(count__gt=1))
        df_aetsa['tsa type'] = 'aeTSA'

        df = pd.concat([df_mtsa_rna,df_mtsa_dna,df_aetsa])
        df = df.rename(columns={'count':'peptides shared with patients'})
        df.to_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/shared_peptide.csv',index = False)

        # df = df.groupby(["patient_id","mutant_peptide_id","tumor_type"]).size().reset_index(name="Counts")
        # df = df.groupby(["mutant_peptide_id","tumor_type"]).size().reset_index(name="peptides shared with patients")
        # df = df.sort_values(by='peptides shared with patients', ascending=False)
        # df = df.loc[(df['peptides shared with patients']>4)]
        # df["TWNeo peptide"] = df["mutant_peptide_id"].apply(lambda x: "TWPEP_" + str(x))
        
        print('success')