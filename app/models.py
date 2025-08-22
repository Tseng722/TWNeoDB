from django.db import models

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
    
    tcr = models.IntegerField(null=True) #1-> immuno, 0->non-immuno, null->no recorded
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
