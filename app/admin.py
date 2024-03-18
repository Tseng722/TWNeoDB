from django.contrib import admin
# from app.models import mtsa_RNA,aeTSA, annotation,opensource,info_patient,bind_mtsa,annotation_mtsa,bind_aetsa,annotation_aetsa,iedb_info
# from app.models import mtsa_pmhc,mtsa_annotation,mtsa_annotation_detail,patient,mtsa_pmhc_annotation_mapping
# from app.models import mtsa_pmhc_patient_mapping,scoring
# from app.models import mtsa_dna_annotation,mtsa_dna_score
from app.models import user_info, user_job
from app.models import mtsa_dna_transcript,mtsa_rna_transcript,patient_info,peptide_selection_score,mutant_peptide,patient_transcript_score,mtsa_dna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mapping,aetsa_transcript


from import_export.admin import ImportExportActionModelAdmin
from import_export import resources

# class mtsaAdmin(ImportExportActionModelAdmin):
#     list_display = ('id','mTumor_protein','mNormal_protein','mAmino_acids_change','mProtein_position','mTpm_normal','mTpm_tumor')

# class mtsaAdmin(ImportExportActionModelAdmin):

#     list_display = ('id','mTumor_protein','mNormal_protein','mAmino_acids_change','mProtein_position','mTpm_normal','mTpm_tumor')


# class aeTSAAdminResource(resources.ModelResource):
#     class Meta:
#          model = aeTSA
#          import_id_fields = ['id']

# class aeTSAAdmin(ImportExportActionModelAdmin):
#     resource_class = aeTSAAdminResource
#     list_display = ('id','peptide')

# class annotationAdminResource(resources.ModelResource):
#     class Meta:
#          model = annotation
#          import_id_fields = ['id']
 
# class annotationAdmin(ImportExportActionModelAdmin):
#     resource_class = annotationAdminResource
#     list_display = ('id','qseq')

# class opensourceAdminResource(resources.ModelResource):
#     class Meta:
#          model = opensource
#          import_id_fields = ['id']
 
# class opensourceAdmin(ImportExportActionModelAdmin):
#     resource_class = opensourceAdminResource
#     list_display = ('id','descriptopn')

# class info_patientAdminResource(resources.ModelResource):
#     class Meta:
#          model = info_patient
#          import_id_fields = ['id']

# class info_patientAdmin(ImportExportActionModelAdmin):
#     resource_class = info_patientAdminResource
#     list_display = ('id','patient')

# class bind_mtsaAdminResource(resources.ModelResource):
#     class Meta:
#          model = bind_mtsa
#          import_id_fields = ['id']

# class bind_mtsaAdmin(ImportExportActionModelAdmin):
#     resource_class = bind_mtsaAdminResource
#     list_display = ('id','tumor_protein')

# class annotation_mtsaAdminResource(resources.ModelResource):
#     class Meta:
#          model = annotation_mtsa
#          import_id_fields = ['id']

# class annotation_mtsaAdmin(ImportExportActionModelAdmin):
#     resource_class = annotation_mtsaAdminResource
#     list_display = ('id','gene_symbol')

# class bind_aetsaAdminResource(resources.ModelResource):
#     class Meta:
#          model = bind_aetsa
#          import_id_fields = ['id']

# class bind_aetsaAdmin(ImportExportActionModelAdmin):
#     resource_class = bind_aetsaAdminResource
#     list_display = ('id','peptide')

# class annotation_aetsaAdminResource(resources.ModelResource):
#     class Meta:
#          model = annotation_aetsa
#          import_id_fields = ['id']

# class annotation_aetsaAdmin(ImportExportActionModelAdmin):
#     resource_class = annotation_aetsaAdminResource
#     list_display = ('id','qseq')

# class iedb_infoAdminResource(resources.ModelResource):
#     class Meta:
#          model = iedb_info
#          import_id_fields = ['id']

# class iedb_infoAdmin(ImportExportActionModelAdmin):
#     resource_class = iedb_infoAdminResource
#     list_display = ('id','description','alleleName')

# ################################################################################s

# class patientAdminResource(resources.ModelResource):
#     class Meta:
#          model = patient
#          import_id_fields = ['id']

# class patientAdmin(ImportExportActionModelAdmin):
#     resource_class = patientAdminResource
#     list_display = ('id','patient')

# class mtsa_pmhcAdminResource(resources.ModelResource):
#     class Meta:
#          model = mtsa_pmhc
#          import_id_fields = ['id']

# class mtsa_pmhcAdmin(ImportExportActionModelAdmin):
#     resource_class = mtsa_pmhcAdminResource
#     list_display = ('id','tumor_protein','hla_type')

# class mtsa_annotationAdminResource(resources.ModelResource):
#     class Meta:
#          model = mtsa_annotation
#          import_id_fields = ['id']

# class mtsa_annotationAdmin(ImportExportActionModelAdmin):
#     resource_class = mtsa_annotationAdminResource
#     list_display = ('id','gene_symbol','transcript_id')

# class mtsa_annotation_detailAdminResource(resources.ModelResource):
#     class Meta:
#          model = mtsa_annotation_detail
#          import_id_fields = ['id']

# class mtsa_annotation_detailAdmin(ImportExportActionModelAdmin):
#     resource_class = mtsa_annotation_detailAdminResource
#     list_display = ('id','vaa_p','patient','variant_position')

# class mtsa_pmhc_annotation_mappingAdminResource(resources.ModelResource):
#     class Meta:
#          model = mtsa_pmhc_annotation_mapping
#          import_id_fields = ['id']

# class mtsa_pmhc_annotation_mappingAdmin(ImportExportActionModelAdmin):
#     resource_class = mtsa_pmhc_annotation_mappingAdminResource
#     list_display = ('id',)

# class mtsa_pmhc_patient_mappingAdminResource(resources.ModelResource):
#     class Meta:
#          model = mtsa_pmhc_patient_mapping
#          import_id_fields = ['id']

# class mtsa_pmhc_patient_mappingAdmin(ImportExportActionModelAdmin):
#     resource_class = mtsa_pmhc_patient_mappingAdminResource
#     list_display = ('id',)

# class scoringAdminResource(resources.ModelResource):
#     class Meta:
#          model = scoring
#          import_id_fields = ['id']

# class scoringAdmin(ImportExportActionModelAdmin):
#     resource_class = scoringAdminResource
#     list_display = ('id',)


# class mtsa_dna_scoreAdminResource(resources.ModelResource):
#     class Meta:
#          model = mtsa_dna_score
#          import_id_fields = ['id']

# class mtsa_dna_scoreAdmin(ImportExportActionModelAdmin):
#     resource_class = mtsa_dna_scoreAdminResource
#     list_display = ('id',)

# class mtsa_dna_annotationAdminResource(resources.ModelResource):
#     class Meta:
#          model = mtsa_dna_annotation
#          import_id_fields = ['id']

# class mtsa_dna_annotationAdmin(ImportExportActionModelAdmin):
#     resource_class = mtsa_dna_annotationAdminResource
#     list_display = ('id',)

# ##################################

class mtsa_dna_transcriptAdminResource(resources.ModelResource):
    class Meta:
         model = mtsa_dna_transcript
         import_id_fields = ['id']

class mtsa_dna_transcriptAdmin(ImportExportActionModelAdmin):
    resource_class = mtsa_dna_transcriptAdminResource
    list_display = ('id',)

class mtsa_rna_transcriptAdminResource(resources.ModelResource):
    class Meta:
         model = mtsa_rna_transcript
         import_id_fields = ['id']

class mtsa_rna_transcriptAdmin(ImportExportActionModelAdmin):
    resource_class = mtsa_rna_transcriptAdminResource
    list_display = ('id',)

class user_infoAdminResource(resources.ModelResource):
    class Meta:
         model = user_info
         import_id_fields = ['id']

class user_infoAdmin(ImportExportActionModelAdmin):
    resource_class = user_infoAdminResource
    list_display = ('id',)

class user_jobAdminResource(resources.ModelResource):
    class Meta:
         model = user_job
         import_id_fields = ['id']

class user_jobAdmin(ImportExportActionModelAdmin):
    resource_class = user_jobAdminResource
    list_display = ('id',)


class patient_infoAdminResource(resources.ModelResource):
    class Meta:
         model = patient_info
         import_id_fields = ['id']

class patient_infoAdmin(ImportExportActionModelAdmin):
    resource_class = patient_infoAdminResource
    list_display = ('id',)
class peptide_selection_scoreAdminResource(resources.ModelResource):
    class Meta:
         model = peptide_selection_score
         import_id_fields = ['id']

class peptide_selection_scoreAdmin(ImportExportActionModelAdmin):
    resource_class = peptide_selection_scoreAdminResource
    list_display = ('id',)
class mutant_peptideAdminResource(resources.ModelResource):
    class Meta:
         model = mutant_peptide
         import_id_fields = ['id']

class mutant_peptideAdmin(ImportExportActionModelAdmin):
    resource_class = mutant_peptideAdminResource
    list_display = ('id',)
class patient_transcript_scoreAdminResource(resources.ModelResource):
    class Meta:
         model = patient_transcript_score
         import_id_fields = ['id']

class patient_transcript_scoreAdmin(ImportExportActionModelAdmin):
    resource_class = patient_transcript_scoreAdminResource
    list_display = ('id',)
class mtsa_dna_transcript_mutant_mappingAdminResource(resources.ModelResource):
    class Meta:
         model = mtsa_dna_transcript_mutant_mapping
         import_id_fields = ['id']

class mtsa_dna_transcript_mutant_mappingAdmin(ImportExportActionModelAdmin):
    resource_class = mtsa_dna_transcript_mutant_mappingAdminResource
    list_display = ('id',)
class mtsa_rna_transcript_mutant_mappingAdminResource(resources.ModelResource):
    class Meta:
         model = mtsa_rna_transcript_mutant_mapping
         import_id_fields = ['id']

class mtsa_rna_transcript_mutant_mappingAdmin(ImportExportActionModelAdmin):
    resource_class = mtsa_rna_transcript_mutant_mappingAdminResource
    list_display = ('id',)


class aetsa_transcriptAdminResource(resources.ModelResource):
    class Meta:
         model = aetsa_transcript
         import_id_fields = ['id']

class aetsa_transcriptAdmin(ImportExportActionModelAdmin):
    resource_class = aetsa_transcriptAdminResource
    list_display = ('id',)


# admin.site.register(mtsa_RNA,mtsaAdmin)
# admin.site.register(aeTSA,aeTSAAdmin)
# admin.site.register(annotation,annotationAdmin)
# admin.site.register(opensource,opensourceAdmin)
# admin.site.register(annotation_aetsa,annotation_aetsaAdmin)
# admin.site.register(annotation_mtsa,annotation_mtsaAdmin)
# admin.site.register(bind_mtsa,bind_mtsaAdmin)
# admin.site.register(bind_aetsa,bind_aetsaAdmin)
# admin.site.register(info_patient,info_patientAdmin)
# admin.site.register(iedb_info,iedb_infoAdmin)
# admin.site.register(patient,patientAdmin)
# admin.site.register(mtsa_pmhc,mtsa_pmhcAdmin)
# admin.site.register(mtsa_annotation,mtsa_annotationAdmin)
# admin.site.register(mtsa_annotation_detail,mtsa_annotation_detailAdmin)
# admin.site.register(mtsa_pmhc_annotation_mapping,mtsa_pmhc_annotation_mappingAdmin)
# admin.site.register(mtsa_pmhc_patient_mapping,mtsa_pmhc_patient_mappingAdmin)
# admin.site.register(scoring,scoringAdmin)
# admin.site.register(mtsa_dna_annotation,mtsa_dna_annotationAdmin)
# admin.site.register(mtsa_dna_score,mtsa_dna_scoreAdmin)


#########################
admin.site.register(user_info,user_infoAdmin)
admin.site.register(user_job,user_jobAdmin)
admin.site.register(mtsa_dna_transcript,mtsa_dna_transcriptAdmin)
admin.site.register(mtsa_rna_transcript,mtsa_rna_transcriptAdmin)
admin.site.register(patient_info,patient_infoAdmin)
admin.site.register(peptide_selection_score,peptide_selection_scoreAdmin)
admin.site.register(mutant_peptide,mutant_peptideAdmin)
admin.site.register(patient_transcript_score,patient_transcript_scoreAdmin)
admin.site.register(mtsa_dna_transcript_mutant_mapping,mtsa_dna_transcript_mutant_mappingAdmin)
admin.site.register(mtsa_rna_transcript_mutant_mapping,mtsa_rna_transcript_mutant_mappingAdmin)
admin.site.register(aetsa_transcript,aetsa_transcriptAdmin)
