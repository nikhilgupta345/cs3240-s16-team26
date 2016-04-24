from django import forms

class DocumentForm(forms.Form):
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
