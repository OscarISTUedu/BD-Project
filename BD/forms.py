from django.forms import forms

from BD.models import Patient


class PatientNameForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["name"]