from django import  forms
from . import models

class UploadTestForm(forms.ModelForm):
    class Meta:
        model = models.Tests
        fields = ('test_name', 'test_file')
