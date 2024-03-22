from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,aetsa_transcript
from app.models import shared_pep_mtsa_rna,shared_pep_mtsa_dna,shared_pep_aetsa,hla_in_patient
from django.forms.models import model_to_dict
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db import connection
import pandas as pd
from django_pandas.io import read_frame
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
from django.conf import settings
import os
BASE_DIR = settings.BASE_DIR
OUT_HTML_DIR = os.path.join(BASE_DIR, 'templates')
class Command(BaseCommand):
    help = 'update_summary'

    # def add_arguments(self, parser):
    # python manage.py update_summary

    def handle(self, *args, **options):
        queryset = hla_in_patient.objects.all()
        df = read_frame(queryset)
        df_a = df.loc[df['class_type']=='A']
        df_a = df_a.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        
        # df_a['hla_type'] = df_a.apply(lambda x: 'Other' if x['patients'] <= 1 else x['hla_type'], axis=1)
        # df_a.reset_index(drop=True, inplace=True)
        # df_other = df_a.loc[df_a['hla_type']=='Other']
        # df_other = df_other.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        # df_a = df_a.loc[df_a['hla_type']!='Other']
        # df_a = pd.concat([df_a,df_other])
        df_a.to_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-a.csv',index = False)
        

        fig_hla_a = px.bar(df_a, x="hla_type", y="patients", color="tumor_type", title="HLA-A type")
        graph_html_hla_a = plot(fig_hla_a, output_type='div')
        with open(OUT_HTML_DIR+'/graph_hla_a.html', 'w') as file:
            file.write(graph_html_hla_a)
        print('hla_a')
        df_b = df.loc[df['class_type']=='B']
        df_b = df_b.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        # df_b['hla_type'] = df_b.apply(lambda x: 'Other' if x['patients'] <= 4 else x['hla_type'], axis=1)
        # df_b.reset_index(drop=True, inplace=True)
        # df_other = df_b.loc[df_b['hla_type']=='Other']
        # df_other = df_other.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        # df_b = df_b.loc[df_b['hla_type']!='Other']
        # df_b = pd.concat([df_b,df_other])

        df_b.to_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-b.csv',index = False)
        fig_hla_b = px.bar(df_b, x="hla_type", y="patients", color="tumor_type", title="HLA-B type")
        graph_html_hla_b = plot(fig_hla_b, output_type='div')
        with open(OUT_HTML_DIR+'/graph_hla_b.html', 'w') as file:
            file.write(graph_html_hla_b)
        print('hla_b')

        df_c = df.loc[df['class_type']=='C']
        df_c = df_c.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        
        # df_c['hla_type'] = df_c.apply(lambda x: 'Other' if x['patients'] <= 4 else x['hla_type'], axis=1)
        # df_c.reset_index(drop=True, inplace=True)
        # df_other = df_c.loc[df_c['hla_type']=='Other']
        # df_other = df_other.groupby(["hla_type","tumor_type"]).size().reset_index(name="patients").sort_values(by='patients', ascending=False)
        # df_c = df_c.loc[df_c['hla_type']!='Other']
        # df_c = pd.concat([df_c,df_other])

        df_c.to_csv('/work1791/cindy2270/web/web_v1/webV1/static/file/hla-c.csv',index = False)
        fig_hla_c = px.bar(df_c, x="hla_type", y="patients", color="tumor_type", title="HLA-C type")
        graph_html_hla_c = plot(fig_hla_c, output_type='div')
        with open(OUT_HTML_DIR+'/graph_hla_c.html', 'w') as file:
            file.write(graph_html_hla_c)
        print('hla_c')

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
        df = df.sort_values(by='peptides shared with patients', ascending=False)
        df = df.loc[(df['peptides shared with patients']>2)]
        df["TWNeo peptide"] = df["mutant_peptide_id"].apply(lambda x: "TWPEP_" + str(x))
        fig = px.bar(df, x="TWNeo peptide",y= 'peptides shared with patients',color="tumor_type")
        graph_html_shared_pep = plot(fig, output_type='div')
        with open(OUT_HTML_DIR+'/graph_shared_pep.html', 'w') as file:
            file.write(graph_html_shared_pep)
        print('shared_pep')
        queryset = patient_info.objects.values("tumor_type").annotate(count=Count('id',distinct=True))
        df_patient_info = read_frame(queryset)
        fig_patient = px.pie(df_patient_info, values='count', names='tumor_type')
        graph_html_patient_info = plot(fig_patient, output_type='div')
        with open(OUT_HTML_DIR+'/graph_patient_info.html', 'w') as file:
            file.write(graph_html_patient_info)
        print('patient_info')

        # df = df.groupby(["patient_id","mutant_peptide_id","tumor_type"]).size().reset_index(name="Counts")
        # df = df.groupby(["mutant_peptide_id","tumor_type"]).size().reset_index(name="peptides shared with patients")
        # df = df.sort_values(by='peptides shared with patients', ascending=False)
        # df = df.loc[(df['peptides shared with patients']>4)]
        # df["TWNeo peptide"] = df["mutant_peptide_id"].apply(lambda x: "TWPEP_" + str(x))
        
        print('success')