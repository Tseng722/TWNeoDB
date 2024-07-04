from django.db import models

# # Create your models here.
# class mtsa_RNA(models.Model):
#     # mTSAid = models.AutoField(primary_key=True)
#     mTumor_protein = models.CharField(max_length=30,null=True)
#     mNormal_protein = models.CharField(max_length=30,null=True)
#     mAmino_acids_change = models.CharField(max_length=5,null=True)
#     mProtein_position = models.IntegerField(null=True)
#     # mFrequency = models.IntegerField(null=True)
#     mTpm_normal = models.FloatField(null=True)
#     mTpm_tumor = models.FloatField(null=True)
#     mTissue_type = models.CharField(max_length=20,null=True)
#     def __str__(self):
#         return self.mTumor_protein

# # class HLA_type(models.Model):
#     mHLA_type = models.CharField(max_length=20,null=True)
#     mIc50 = models.FloatField(null=True)
#     mMT = models.FloatField(null=True)
#     # def __str__(self):
#     #     return self.mHLA_type
        
# # class Gene(models.Model):
#     mGene_symbol = models.CharField(max_length=30,null=True)
#     mWildtype_protein = models.CharField(max_length=2000,null=True)
#     mGene_id = models.CharField(max_length=30,null=True)
#     mTranscript_id = models.CharField(max_length=30,null=True)
#     mProtein_id = models.CharField(max_length=30,null=True)
#     mVariant_position = models.CharField(max_length=30,null=True)
#     mReference = models.CharField(max_length=5,null=True)
#     mAltered = models.CharField(max_length=5,null=True)
#     # def __str__(self):
#     #     return self.mGene_symbol
# class aeTSA(models.Model):
#     id = models.IntegerField(primary_key=True)
#     # aeTSA_id =  models.AutoField(primary_key=True)
#     peptide = models.CharField(max_length=100,null=True)
#     aHLA_type = models.CharField(max_length=20,null=True)
#     aIc50 = models.FloatField(null=True)
#     aMT = models.FloatField(null=True)
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         db_table = 'aeTSA'
# class annotation(models.Model):    
#     id = models.IntegerField(primary_key=True)
#     # ann_id = models.AutoField(primary_key=True)
#     qseq = models.CharField(max_length=100,null=True)
#     sseq_nucl = models.CharField(max_length=100,null=True)
#     sseq_nucl_interval = models.CharField(max_length=100,null=True)
#     T_read_count = models.IntegerField(null=True)
#     T_qseq_total_read = models.IntegerField(null=True)
#     T_avg_depth = models.IntegerField(null=True)
#     T_translated_pep = models.CharField(max_length=100,null=True)
#     aGene = models.CharField(max_length=100,null=True)
#     Element = models.CharField(max_length=100,null=True)
#     expected_T_N_read_count = models.IntegerField(null=True)
#     expected_element_read_count = models.IntegerField(null=True)
#     Element_read_proportion = models.FloatField(null=True)
#     aeTSAid = models.ForeignKey(aeTSA,  db_column='aeTSAid', blank=True, null=True,on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         db_table = 'annotation'
# class opensource(models.Model):    
#     id = models.IntegerField(primary_key=True)
#     # patient_id = models.AutoField(primary_key=True)
#     biosample = models.CharField(max_length=100,null=True)
#     tumor_type = models.CharField(max_length=100,null=True)
#     descriptopn =  models.CharField(max_length=100,null=True)
#     annid = models.ForeignKey(annotation,  db_column='annid', blank=True, null=True,on_delete=models.CASCADE)
#     aeTSAid = models.ForeignKey(aeTSA,  db_column='aeTSAid', blank=True, null=True,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         db_table = 'opensource'

# #############################################################

# class info_patient(models.Model):   
#     id	= models.IntegerField(primary_key=True)
#     patient	= models.CharField(max_length=20,null=True)
#     sample_from	= models.CharField(max_length=20,null=True)
#     tumor_type	= models.CharField(max_length=20,null=True)
#     descriptopn	= models.CharField(max_length=30,null=True)
#     source = models.CharField(max_length=10,null=True)
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         db_table = 'info_patient'


# class bind_mtsa(models.Model):   
#     id = models.IntegerField(primary_key=True)
#     tumor_protein = models.CharField(max_length=30,null=True)
#     normal_protein = models.CharField(max_length=30,null=True)
#     hla_type = models.CharField(max_length=20,null=True)
#     ic50= models.FloatField(null=True)
#     mt = models.FloatField(null=True)
#     info_patient_id = models.ForeignKey(info_patient,null=True,on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         # unique_together = [('tumor_protein', 'hla_type')]
#         db_table = 'bind_mtsa'

# class annotation_mtsa(models.Model):   
#     id = models.IntegerField(primary_key=True)
#     gene_symbol = models.CharField(max_length=30,null=True)
#     wildtype_protein = models.TextField(null=True)
#     gene_id = models.CharField(max_length=2000,null=True)
#     transcript_id = models.CharField(max_length=50,null=True)
#     protein_id = models.CharField(max_length=50,null=True)
#     variant_position = models.CharField(max_length=30,null=True)
#     allele_ref = models.CharField(max_length=10,null=True)
#     allele_tumor = models.CharField(max_length=10,null=True)
#     amino_acids_change = models.CharField(max_length=10,null=True)
#     protein_position = models.IntegerField(null=True)
#     tpm_normal = models.FloatField(null=True)
#     tpm_tumor = models.FloatField(null=True)
#     bind_mtsa_id = models.ForeignKey(bind_mtsa,null=True,on_delete=models.CASCADE)
#     info_patient_id = models.ForeignKey(info_patient,null=True,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         db_table = 'annotation_mtsa'


# class bind_aetsa(models.Model):   
#     id = models.IntegerField(primary_key=True)
#     peptide = models.CharField(max_length=30,null=True)
#     hla_type = models.CharField(max_length=20,null=True)
#     ic50= models.FloatField(null=True)
#     mt = models.FloatField(null=True)
#     info_patient_id = models.ForeignKey(info_patient,null=True,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         # unique_together = [('peptide', 'hla_type')]
#         db_table = 'bind_aetsa'

# class annotation_aetsa(models.Model): 
#     id = models.IntegerField(primary_key=True)
#     qseq = models.CharField(max_length=100,null=True)
#     sseq_nucl = models.CharField(max_length=100,null=True)
#     sseq_nucl_interval = models.CharField(max_length=100,null=True)
#     T_read_count = models.IntegerField(null=True)
#     T_qseq_total_read = models.IntegerField(null=True)
#     T_avg_depth = models.IntegerField(null=True)
#     T_translated_pep = models.CharField(max_length=100,null=True)
#     aGene = models.CharField(max_length=100,null=True)
#     Element = models.CharField(max_length=100,null=True)
#     expected_T_N_read_count = models.IntegerField(null=True)
#     expected_element_read_count = models.IntegerField(null=True)
#     Element_read_proportion = models.FloatField(null=True)
#     bind_aetsa_id = models.ForeignKey(bind_aetsa,null=True,on_delete=models.CASCADE)
#     info_patient_id = models.ForeignKey(info_patient,null=True,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         db_table = 'annotation_aetsa'

# class iedb_info(models.Model):
#     id = models.IntegerField(primary_key=True)
#     objectType = models.CharField(max_length=50,null=True)
#     description = models.CharField(max_length=50,null=True)
#     startingPosition = models.IntegerField(null=True)
#     endingPosition = models.IntegerField(null=True)
#     antigenName = models.CharField(max_length=50,null=True)
#     alleleName = models.CharField(max_length=50,null=True)
#     pubMedID = models.CharField(max_length=50,null=True)
#     authors = models.CharField(max_length=100,null=True)
#     journal = models.CharField(max_length=50,null=True)
#     date = models.IntegerField(null=True)
#     title = models.CharField(max_length=50,null=True)


# #############################################################
# class patient(models.Model):
#     id = models.IntegerField()
#     patient	= models.CharField(max_length=50,primary_key=True)
#     sample_from	= models.CharField(max_length=20,null=True)
#     tumor_type	= models.CharField(max_length=20,null=True)
#     descriptopn	= models.CharField(max_length=30,null=True)
#     source = models.CharField(max_length=10,null=True)
#     TSA_type = models.CharField(max_length=10,null=True) #有問題
#     def __str__(self):
#         return str(self.patient)
#     class Meta:
#         managed = True
#         db_table = 'patient'



# class mtsa_annotation(models.Model):
#     id = models.IntegerField()
#     gene_symbol = models.CharField(max_length=30,null=True)
#     wildtype_protein = models.TextField(null=True)
#     gene_id = models.CharField(max_length=2000,null=True)
#     transcript_id = models.CharField(max_length=50,primary_key=True)
#     # variant_position = models.CharField(max_length=30,null=True)
#     # allele_ref = models.CharField(max_length=10,null=True)
#     # allele_tumor = models.CharField(max_length=10,null=True)
#     # vaa = models.CharField(max_length=40,primary_key=True)
#     def __str__(self):
#         return str(self.transcript_id)
#     class Meta:
#         indexes = [
#             models.Index(fields=['gene_symbol']),  
#         ]
#         managed = True
#         # unique_together = [('tumor_protein', 'hla_type')]
#         db_table = 'mtsa_annotation'
# class scoring(models.Model):
#     id = models.IntegerField()
#     ic50= models.FloatField(null=True)
#     mt = models.FloatField(null=True)
#     th = models.CharField(max_length=40,primary_key=True)
#     best_cleavage_position	= models.IntegerField(null=True)
#     best_cleavage_score	= models.FloatField(null=True)
#     predicted_stability	= models.FloatField(null=True)
#     half_life	= models.FloatField(null=True)
#     stability_rank= models.FloatField(null=True)
#     hydro_avg_score = models.FloatField(null=True)
#     foreignness_score = models.FloatField(null=True)
#     IEDB_anno = models.CharField(max_length=255,null=True)
#     dissimilarity = models.FloatField(null=True)
#     cterm_7mer_gravy_score = models.FloatField(null=True)
#     max_7mer_gravy_score = models.FloatField(null=True)
#     length = models.IntegerField(null=True)
#     def __str__(self):
#         return str(self.th)
#     class Meta:
#         managed = True
#         db_table = 'scoring'
        
# class mtsa_pmhc(models.Model):
#     id = models.IntegerField()
#     tumor_protein = models.CharField(max_length=30,null=True)
#     normal_protein = models.CharField(max_length=30,null=True)
#     length = models.IntegerField(null=True)
#     amino_acids_change = models.CharField(max_length=10,null=True)
#     hla_type = models.CharField(max_length=20,null=True)
#     tnh = models.CharField(max_length=40,primary_key=True)
#     th = models.ForeignKey(scoring,to_field='th',null=True, on_delete=models.CASCADE)
    
#     # vaa = models.ForeignKey(mtsa_annotation,null=True,on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.tnh)
#     class Meta:
#         managed = True
#         indexes = [
#             models.Index(fields=['tumor_protein']), 
#             models.Index(fields=['hla_type']),   
#         ]
#         # unique_together = [('tumor_protein', 'hla_type')]
#         db_table = 'mtsa_pmhc'

# class mtsa_annotation_detail(models.Model):
#     id = models.IntegerField()
#     variant_position = models.CharField(max_length=30,null=True)
#     allele_ref = models.CharField(max_length=10,null=True)
#     allele_tumor = models.CharField(max_length=10,null=True)
#     amino_acids_change = models.CharField(max_length=10,null=True)
#     protein_position = models.IntegerField(null=True)
#     tpm_normal = models.FloatField(null=True)
#     tpm_tumor = models.FloatField(null=True)
#     # vaa = models.ForeignKey(mtsa_annotation,null=True,on_delete=models.CASCADE)
#     patient = models.ForeignKey(patient,null=True,on_delete=models.CASCADE)
#     vaa_p = models.CharField(max_length=100,primary_key=True)
#     def __str__(self):
#         return str(self.vaa_p)
#     class Meta:
#         managed = True
#         # unique_together = [('vaa', 'patient')]
#         db_table = 'mtsa_annotation_detail'


# class mtsa_pmhc_annotation_mapping(models.Model):
#     id = models.AutoField(primary_key=True)
#     tnh = models.ForeignKey(mtsa_pmhc,null=True,on_delete=models.CASCADE)
#     transcript_id = models.ForeignKey(mtsa_annotation,null=True,on_delete=models.CASCADE)
#     # vaa = models.ForeignKey(mtsa_annotation,null=True,on_delete=models.CASCADE)
#     patient = models.ForeignKey(patient,null=True,on_delete=models.CASCADE)
#     # vaa_p = models.ForeignKey(mtsa_annotation_detail,null=True,on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         # unique_together = [('tumor_protein', 'hla_type')]
#         db_table = 'mtsa_pmhc_annotation_mapping'

# class mtsa_pmhc_patient_mapping(models.Model):
#     id = models.AutoField(primary_key=True)
#     tnh = models.ForeignKey(mtsa_pmhc,null=True,on_delete=models.CASCADE)
#     # patient = models.ForeignKey(patient,null=True,on_delete=models.CASCADE)
#     transcript_id = models.ForeignKey(mtsa_annotation,null=True,on_delete=models.CASCADE)
#     vaa_p = models.ForeignKey(mtsa_annotation_detail,null=True,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         # unique_together = [('tumor_protein', 'hla_type')]
#         db_table = 'mtsa_pmhc_patient_mapping'

class user_info(models.Model):
    id = models.AutoField(primary_key=True)
    mail=models.EmailField(max_length=254,unique=True)
    ip=models.CharField(max_length=25,null=True)
    country=models.CharField(max_length=50,null=True)
    enroll_time = models.DateTimeField(auto_now_add=True,null=True)
    mail_uuid = models.CharField(max_length=100,unique=True,null=True)
    is_activate = models.IntegerField(null=False,default=0)
    activate_time = models.DateTimeField(null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        db_table = 'user_info'

class user_job(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=100,unique=True)
    start_time = models.DateTimeField(auto_now_add=True,null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=10,default='WAITING')
    # task_id = models.CharField(max_length=100,default='WAITING',null=True)
    user=models.ForeignKey(user_info,null=True,on_delete=models.CASCADE)
    pep_count = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        db_table = 'user_job'

# class mtsa_dna_score(models.Model):
#     id = models.AutoField(primary_key=True)
#     hla_type = models.CharField(max_length=20,null=True)
#     tomur_seq = models.CharField(max_length=30,null=True)
#     best_cleavage_position	= models.IntegerField(null=True)
#     best_cleavage_score	= models.FloatField(null=True)
#     predicted_stability	= models.FloatField(null=True)
#     half_life	= models.FloatField(null=True)
#     stability_rank= models.FloatField(null=True)
#     hydro_avg_score = models.FloatField(null=True)
#     foreignness_score = models.FloatField(null=True)
#     IEDB_anno = models.CharField(max_length=255,null=True)
#     dissimilarity = models.FloatField(null=True)
#     cterm_7mer_gravy_score = models.FloatField(null=True)
#     max_7mer_gravy_score = models.FloatField(null=True)
#     length = models.IntegerField(null=True)
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         unique_together = [('tomur_seq', 'hla_type')]
#         db_table = 'mtsa_dna_score'


# class mtsa_dna_annotation(models.Model):
#     id = models.AutoField(primary_key=True)
#     transcript_id = models.CharField(max_length=30,null=True)
#     gene_symbol	 = models.CharField(max_length=20,null=True)
#     gene_id = models.CharField(max_length=30,null=True)
#     variant_type  = models.CharField(max_length=20,null=True)
#     mutation = models.CharField(max_length=20,null=True)
#     protein_position = models.CharField(max_length=20,null=True)
#     ic50_mut = models.FloatField(null=True)
#     ic50_wild = models.FloatField(null=True)
#     percent_mut = models.FloatField(null=True)
#     percent_wild = models.FloatField(null=True)
#     chromosome = models.CharField(max_length=20,null=True)
#     start = models.IntegerField(null=True)
#     stop = models.IntegerField(null=True)
#     reference 	= models.CharField(max_length=10,null=True)
#     variant = models.CharField(max_length=10,null=True)
#     pos = models.IntegerField(null=True)
#     hla_type = models.CharField(max_length=20,null=True)
#     tomur_seq = models.CharField(max_length=30,null=True)
#     normal_seq = models.CharField(max_length=30,null=True)
#     score_id = models.ForeignKey(mtsa_dna_score,to_field='id',null=True, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return str(self.id)
#     class Meta:
#         managed = True
#         db_table = 'mtsa_dna_annotation'

#############################
class patient_info(models.Model):
    id = models.AutoField(primary_key=True)
    sample_from	= models.CharField(max_length=20,null=True)
    tumor_type	= models.CharField(max_length=20,null=True)
    patient_number	= models.CharField(max_length=30,null=True)
    source = models.CharField(max_length=10,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('sample_from', 'patient_number')]
        db_table = 'patient_info'
    

class mtsa_rna_transcript(models.Model):
    id = models.AutoField(primary_key=True)
    gene_id = models.CharField(max_length=50,null=True)
    transcript_id = models.CharField(max_length=50)
    gene_symbol = models.CharField(max_length=30,null=True)
    variant_position = models.CharField(max_length=50,null=True)
    allele_ref = models.CharField(max_length=10,null=True)
    allele_tumor = models.CharField(max_length=10,null=True)
    amino_acids_change = models.CharField(max_length=10,null=True)
    protein_position = models.IntegerField(null=True)
    wildtype_protein = models.TextField(null=True)
    variant_frequency = models.IntegerField(null=True)
    # tumor_type	= models.CharField(max_length=20,null=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('variant_position', 'allele_ref','allele_tumor')]
        db_table = 'mtsa_rna_transcript'
    
class mtsa_dna_transcript(models.Model):
    id = models.AutoField(primary_key=True)
    gene_id = models.CharField(max_length=50,null=True)
    transcript_id = models.CharField(max_length=50)
    gene_symbol = models.CharField(max_length=30,null=True)
    chromosome = models.CharField(max_length=25,null=True)
    start = models.IntegerField(null=True)
    stop = models.IntegerField(null=True)
    reference = models.CharField(max_length=400,null=True)
    variant = models.CharField(max_length=400,null=True)
    mutation = models.CharField(max_length=20,null=True)
    protein_position = models.CharField(max_length=20,null=True)
    variant_type  = models.CharField(max_length=20,null=True)
    variant_frequency = models.IntegerField(null=True)
    # tumor_type	= models.CharField(max_length=20,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('chromosome', 'start','stop','reference','variant')]
        db_table = 'mtsa_dna_transcript'
        indexes = [
            models.Index(fields=['gene_symbol']), 
        ]

class patient_transcript_score(models.Model):
    id = models.AutoField(primary_key=True)
    tpm_normal = models.FloatField(null=True)
    tpm_tumor = models.FloatField(null=True)
    fold_change = models.FloatField(null=True)
    tumor_dna_depth = models.IntegerField(null=True)
    tumor_dna_vaf = models.FloatField(null=True)
    patient_id = models.ForeignKey(patient_info,to_field='id', on_delete=models.CASCADE)
    rna_id = models.ForeignKey(mtsa_rna_transcript,to_field='id',null=True, on_delete=models.CASCADE,related_name='patient_transcript_score_r')
    dna_id = models.ForeignKey(mtsa_dna_transcript,to_field='id',null=True, on_delete=models.CASCADE,related_name='patient_transcript_score_d')
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('rna_id', 'dna_id','patient_id')]
        db_table = 'patient_transcript_score'

class validated_peptide(models.Model):
    id = models.AutoField(primary_key=True)
    tumor_protein = models.CharField(max_length=30,null=True)
    hla_type = models.CharField(max_length=20,null=True)
    
    pmhc = models.IntegerField(null=True)
    ieltas = models.IntegerField(null=True)
    iedb_mhc = models.IntegerField(null=True)
    
    tcr = models.IntegerField(null=True)
    deepneo = models.IntegerField(null=True)
    iedb_tcr = models.IntegerField(null=True)
    prime = models.IntegerField(null=True)

    best_cleavage_position	= models.IntegerField(null=True)
    best_cleavage_score	= models.FloatField(null=True)
    predicted_stability	= models.FloatField(null=True)
    half_life	= models.FloatField(null=True)
    stability_rank= models.FloatField(null=True)
    hydro_avg_score = models.FloatField(null=True)
    foreignness_score = models.FloatField(null=True)
    IEDB_anno = models.CharField(max_length=255,null=True)
    dissimilarity = models.FloatField(null=True)
    cterm_7mer_gravy_score = models.FloatField(null=True)
    max_7mer_gravy_score = models.FloatField(null=True)
    length = models.IntegerField(null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('tumor_protein','hla_type')]
        db_table = 'validated_peptide'
        indexes = [
            models.Index(fields=['tumor_protein','hla_type']), 
        ]

class peptide_selection_score(models.Model):
    id = models.AutoField(primary_key=True)
    tumor_protein = models.CharField(max_length=30,null=True)
    hla_type = models.CharField(max_length=20,null=True)
    best_cleavage_position	= models.IntegerField(null=True)
    best_cleavage_score	= models.FloatField(null=True)
    predicted_stability	= models.FloatField(null=True)
    half_life	= models.FloatField(null=True)
    stability_rank= models.FloatField(null=True)
    hydro_avg_score = models.FloatField(null=True)
    foreignness_score = models.FloatField(null=True)
    IEDB_anno = models.CharField(max_length=255,null=True)
    dissimilarity = models.FloatField(null=True)
    cterm_7mer_gravy_score = models.FloatField(null=True)
    max_7mer_gravy_score = models.FloatField(null=True)
    length = models.IntegerField(null=True)
    validated_peptide_id = models.ForeignKey(validated_peptide,to_field='id',null=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('tumor_protein','hla_type')]
        db_table = 'peptide_selection_score'
        indexes = [
            models.Index(fields=['tumor_protein','hla_type']), 
        ]
        
class mutant_peptide(models.Model):
    id = models.AutoField(primary_key=True)
    tumor_protein = models.CharField(max_length=30,null=True)
    normal_protein = models.CharField(max_length=30,null=True)
    hla_type = models.CharField(max_length=20,null=True)
    length = models.IntegerField(null=True)
    amino_acids_change = models.CharField(max_length=10,null=True)
    pos = models.CharField(max_length=20,null=True)
    ic50_mut = models.FloatField(null=True)
    ic50_wild = models.FloatField(null=True)
    percent_mut = models.FloatField(null=True)
    percent_wild = models.FloatField(null=True)
    peptide_selection_score_id = models.ForeignKey(peptide_selection_score,to_field='id',null=True, on_delete=models.CASCADE, related_name='mutant_peptide')
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('tumor_protein', 'normal_protein','hla_type')]
        db_table = 'mutant_peptide'
        indexes = [
            models.Index(fields=['tumor_protein','hla_type']), 
            models.Index(fields=['tumor_protein']), 
            models.Index(fields=['hla_type']),   
        ]

class mtsa_rna_transcript_mutant_mapping(models.Model):
    id = models.AutoField(primary_key=True)
    mtsa_rna_transcript_id = models.ForeignKey(mtsa_rna_transcript,to_field='id', on_delete=models.CASCADE)
    mutant_peptide_id = models.ForeignKey(mutant_peptide,to_field='id', on_delete=models.CASCADE)
    tumor_type	= models.CharField(max_length=20,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('mtsa_rna_transcript_id', 'mutant_peptide_id','tumor_type')]
        db_table = 'mtsa_rna_transcript_mutant_mapping'

class mtsa_dna_transcript_mutant_mapping(models.Model):
    id = models.AutoField(primary_key=True)
    mtsa_dna_transcript_id = models.ForeignKey(mtsa_dna_transcript,to_field='id', on_delete=models.CASCADE)
    mutant_peptide_id = models.ForeignKey(mutant_peptide,to_field='id', on_delete=models.CASCADE)
    tumor_type	= models.CharField(max_length=20,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('mtsa_dna_transcript_id', 'mutant_peptide_id','tumor_type')]
        db_table = 'mtsa_dna_transcript_mutant_mapping'

class aetsa_transcript(models.Model):
    id = models.AutoField(primary_key=True)
    translated_tumor_peptide = models.CharField(max_length=100,null=True)
    gene_id = models.CharField(max_length=50,null=True)
    gene_symbol = models.CharField(max_length=30,null=True)
    gene_element = models.CharField(max_length=50,null=True)
    cdna_location = models.CharField(max_length=80,null=True)
    cdna_sequence = models.TextField(null=True)
    putative_neoantigen_type = models.CharField(max_length=10,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('translated_tumor_peptide', 'cdna_location','gene_element')]
        indexes = [
            models.Index(fields=['gene_symbol']), 
            # models.Index(fields=['hla_type']),   
        ]
        db_table = 'aetsa_transcript'

class patient_aetsa_score(models.Model):
    id = models.AutoField(primary_key=True)
    tumor_read_count = models.IntegerField(null=True)
    normal_read_count = models.IntegerField(null=True)
    sum_of_tumor_and_normal_read_count = models.IntegerField(null=True)
    total_tumor_read_count = models.IntegerField(null=True)
    total_normal_read_count = models.IntegerField(null=True)
    sum_of_total_tumor_and_normal_read_count = models.IntegerField(null=True)
    tumor_average_read_depth = models.FloatField(null=True)
    normal_average_read_depth = models.FloatField(null=True)
    sum_of_expected_read_count = models.IntegerField(null=True)
    average_depth_ratio = models.FloatField(null=True)
    element_read_proportion = models.FloatField(null=True)
    sum_of_element_read_count = models.IntegerField(null=True)
    aetsa_id = models.ForeignKey(aetsa_transcript,to_field='id',null=True, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(patient_info,to_field='id', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        
        unique_together = [
            ("patient_id","aetsa_id","tumor_read_count", "normal_read_count", "sum_of_tumor_and_normal_read_count", "total_tumor_read_count", "total_normal_read_count", "sum_of_total_tumor_and_normal_read_count", "tumor_average_read_depth", "normal_average_read_depth", "sum_of_expected_read_count", "average_depth_ratio", "element_read_proportion", "sum_of_element_read_count")
        ]
        db_table = 'patient_aetsa_score'

class aetsa_transcript_mutant_mapping(models.Model):
    id = models.AutoField(primary_key=True)
    aetsa_transcript_id = models.ForeignKey(aetsa_transcript,to_field='id',null=True, on_delete=models.CASCADE)
    mutant_peptide_id = models.ForeignKey(mutant_peptide,to_field='id', on_delete=models.CASCADE)
    tumor_type	= models.CharField(max_length=20,null=True)
    
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('aetsa_transcript_id', 'mutant_peptide_id','tumor_type')]
        db_table = 'aetsa_transcript_mutant_mapping'

class hla_in_patient(models.Model):
    id = models.AutoField(primary_key=True)
    hla_type = models.CharField(max_length=20,null=True)
    class_type = models.CharField(max_length=5,null=True)
    # patient_number	= models.CharField(max_length=30,null=True)
    patient_id = models.ForeignKey(patient_info,to_field='id', null=True,on_delete=models.CASCADE)
    tumor_type	= models.CharField(max_length=20,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('hla_type', 'patient_id')]
        db_table = 'hla_in_patient'


class shared_pep_in_patient(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(patient_info,to_field='id', null=True,on_delete=models.CASCADE)
    rna_id = models.ForeignKey(mtsa_rna_transcript,to_field='id',null=True, on_delete=models.CASCADE)
    dna_id = models.ForeignKey(mtsa_dna_transcript,to_field='id',null=True, on_delete=models.CASCADE)
    aetsa_id = models.ForeignKey(aetsa_transcript,to_field='id',null=True, on_delete=models.CASCADE)
    mutant_peptide_id = models.ForeignKey(mutant_peptide,to_field='id',null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('patient_id','rna_id','dna_id','aetsa_id','mutant_peptide_id')]
        db_table = 'shared_pep_in_patient'
    
    
class shared_pep_mtsa_rna(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(patient_info,to_field='id', null=True,on_delete=models.CASCADE)
    rna_id = models.ForeignKey(mtsa_rna_transcript,to_field='id',null=True, on_delete=models.CASCADE)
    mutant_peptide_id = models.ForeignKey(mutant_peptide,to_field='id',null=True, on_delete=models.CASCADE)
    tumor_type	= models.CharField(max_length=20,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('patient_id','rna_id','mutant_peptide_id')]
        db_table = 'shared_pep_mtsa_rna'
   
class shared_pep_mtsa_dna(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(patient_info,to_field='id', null=True,on_delete=models.CASCADE)
    dna_id = models.ForeignKey(mtsa_dna_transcript,to_field='id',null=True, on_delete=models.CASCADE)
    mutant_peptide_id = models.ForeignKey(mutant_peptide,to_field='id',null=True, on_delete=models.CASCADE)
    tumor_type	= models.CharField(max_length=20,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('patient_id','dna_id','mutant_peptide_id')]
        db_table = 'shared_pep_mtsa_dna'
   
class shared_pep_aetsa(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(patient_info,to_field='id', null=True,on_delete=models.CASCADE)
    aetsa_id = models.ForeignKey(aetsa_transcript,to_field='id',null=True, on_delete=models.CASCADE)
    mutant_peptide_id = models.ForeignKey(mutant_peptide,to_field='id',null=True, on_delete=models.CASCADE)
    tumor_type	= models.CharField(max_length=20,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        managed = True
        unique_together = [('patient_id','aetsa_id','mutant_peptide_id')]
        db_table = 'shared_pep_aetsa'
