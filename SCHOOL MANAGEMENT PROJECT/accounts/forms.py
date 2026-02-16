from django import forms
from .models import School

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'code', 'address']

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if School.objects.filter(code=code).exists():
            raise forms.ValidationError("⚠️ School code already exists")
        return code