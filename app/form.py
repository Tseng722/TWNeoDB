from django import forms

class searchmTSAForm(forms.Form):
    ptumor_protein = forms.CharField(max_length=50, initial='',required=False,widget=forms.TextInput(attrs={'class': 'input'}))
    ptissue_type = forms.CharField(max_length=20, initial='',required=False,widget=forms.TextInput(attrs={'class': 'input'}))
    psource = forms.CharField(max_length=10, initial='',required=False,widget=forms.TextInput(attrs={'class': 'input'}))
    pgene_symbol = forms.CharField(max_length=20, initial='',required=False,widget=forms.TextInput(attrs={'class': 'input'}))
    phla_type = forms.CharField(max_length=10, initial='',required=False,widget=forms.TextInput(attrs={'class': 'input'}))
    