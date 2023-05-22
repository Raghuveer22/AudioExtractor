from django import forms

class SongUploadForm(forms.Form):
    url = forms.URLField()
    file = forms.FileField()
    def is_valid(self):
        valid = super().is_valid()
        if 'url' in self.cleaned_data or 'file' in self.cleaned_data:
            valid = True
        if 'url' in self.cleaned_data and 'file' in self.cleaned_data:
            self.add_error(None, 'Please fill out only one field.')
            valid = False
        return valid