from django import forms

class DocumentForm(forms.Form):
    #name = forms.CharField(max_length=128, label='Report Name')
    #description = forms.CharField(max_length=128, label='Short Description')
    #docfile = forms.FileField(label='Select a file')

    fname = forms.CharField(
        label='File Name:',
        max_length=128
    )
    docfile = forms.FileField(
        label='Upload File:'
    )
    encrypted = forms.BooleanField(
        label='Mark as Encrypted:'
    )


class SearchReportsForm(forms.Form):
    all = forms.CharField(max_length=128, initial="", required=False)
    name = forms.CharField(max_length=128, initial="", required=False)
    short_desc = forms.CharField(max_length=128, initial="", required=False)
    long_desc = forms.CharField(max_length=128, initial="", required=False)
    owner = forms.CharField(max_length=128, initial="", required=False)
    num_results = forms.IntegerField(required=False)
