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
    keyword = forms.CharField(max_length=128, required=False)
    name = forms.CharField(max_length=128, required=False)
    #owner = forms.CharField(max_length=128, required=False)
    short_desc = forms.CharField(max_length=120, required=False)
