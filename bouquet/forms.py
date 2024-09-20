from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['client_name', 'phone_number']