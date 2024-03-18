import django_filters
# from app.models import mtsa_RNA,info_patient,bind_mtsa,annotation_mtsa,bind_aetsa,annotation_aetsa
# from app.models import mtsa_pmhc,mtsa_annotation,mtsa_annotation_detail,patient,mtsa_pmhc_annotation_mapping
# from app.models import mtsa_pmhc_annotation_mapping,mtsa_pmhc_patient_mapping
from django import forms

# class mTSAFilter(django_filters.FilterSet):#可刪
#     mTumor_protein = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input'}))
#     mTissue_type = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     source = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'input1'}))
#     mGene_symbol = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     mHLA_type = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     mIc50_min = django_filters.IsoDateTimeFilter(widget=forms.TextInput(attrs={'class': 'input'}))
#     mIc50_max = django_filters.IsoDateTimeFilter(widget=forms.TextInput(attrs={'class': 'input'}))
#     mMT_min = django_filters.IsoDateTimeFilter(widget=forms.TextInput(attrs={'class': 'input'}))
#     mMT_max = django_filters.IsoDateTimeFilter(widget=forms.TextInput(attrs={'class': 'input'}))
    
#     class Meta:
#         model = mtsa_RNA
#         fields = '__all__'


# class mtsaFilter1(django_filters.FilterSet): #可刪
#     tumor_protein = django_filters.CharFilter(field_name='bind_mtsa_id__tumor_protein',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input'}))
#     tumor_type = django_filters.CharFilter(field_name='bind_mtsa_id__info_patient_id__tumor_type',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     source = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'input1'}))
#     gene_symbol = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     hla_type = django_filters.CharFilter(field_name='bind_mtsa_id__hla_type',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     ic50_min = django_filters.IsoDateTimeFilter(field_name='bind_mtsa_id__ic50',widget=forms.TextInput(attrs={'class': 'input'}))
#     ic50_max = django_filters.IsoDateTimeFilter(field_name='bind_mtsa_id__ic50',widget=forms.TextInput(attrs={'class': 'input'}))
#     mt_min = django_filters.IsoDateTimeFilter(field_name='bind_mtsa_id__mt',widget=forms.TextInput(attrs={'class': 'input'}))
#     mt_max = django_filters.IsoDateTimeFilter(field_name='bind_mtsa_id__mt',widget=forms.TextInput(attrs={'class': 'input'}))
 
    
#     class Meta:
#         model = annotation_mtsa
#         fields = '__all__'


# class aetsaFilter(django_filters.FilterSet):
#     peptide = django_filters.CharFilter(field_name='peptide',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input'}))
#     hla_type = hla_type = django_filters.CharFilter(field_name='hla_type',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     tumor_type = django_filters.CharFilter(field_name='info_patient_id__tumor_type',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))


# class mtsaFilter(django_filters.FilterSet):
#     tumor_protein = django_filters.CharFilter(field_name='tnh__tumor_protein',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input'}))
#     tumor_type = django_filters.CharFilter(field_name='patient__tumor_type',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     source = django_filters.CharFilter(field_name='patient__source',widget=forms.TextInput(attrs={'class': 'input1'}))
#     gene_symbol = django_filters.CharFilter(field_name='transcript_id__gene_symbol',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     hla_type = django_filters.CharFilter(field_name='tnh__hla_type',lookup_expr='icontains',widget=forms.TextInput(attrs={'class': 'input1'}))
#     ic50_min = django_filters.IsoDateTimeFilter(field_name='tnh__ic50',widget=forms.TextInput(attrs={'class': 'input'}))
#     ic50_max = django_filters.IsoDateTimeFilter(field_name='tnh__ic50',widget=forms.TextInput(attrs={'class': 'input'}))
#     mt_min = django_filters.IsoDateTimeFilter(field_name='tnh__mt',widget=forms.TextInput(attrs={'class': 'input'}))
#     mt_max = django_filters.IsoDateTimeFilter(field_name='tnh__mt',widget=forms.TextInput(attrs={'class': 'input'}))
 
    
#     class Meta:
#         model = mtsa_pmhc_annotation_mapping
#         fields = '__all__'
