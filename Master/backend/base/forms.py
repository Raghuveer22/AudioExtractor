from django import forms

class SongUploadForm(forms.Form):
    url = forms.URLField()
    file = forms.FileField()
    