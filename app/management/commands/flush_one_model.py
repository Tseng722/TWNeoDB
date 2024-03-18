from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,aetsa_transcript_mutant_mapping,patient_aetsa_score,aetsa_transcript,hla_in_patient,validated_peptide

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = 'delete selected model'

    # def add_arguments(self, parser):
    # python manage.py flush_one_model

    def handle(self, *args, **options):
        # mtsa_rna_transcript.objects.all().delete()
        # mtsa_dna_transcript.objects.all().delete()
        # patient_info.objects.all().delete()
        # peptide_selection_score.objects.all().delete()
        # mutant_peptide.objects.all().delete()
        # patient_transcript_score.objects.all().delete()
        # mtsa_dna_transcript_mutant_mapping.objects.all().delete()
        # mtsa_rna_transcript_mutant_mapping.objects.all().delete()
        # hla_in_patient.objects.all().delete()
        validated_peptide.objects.all().delete()
        print('success')


        # patient_instance = patient.objects.get(patient = 'colon172_mtsa_022T')
        # print(patient_instance.source)
