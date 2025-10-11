from django import forms
from .models import Patient, Prescription, Medication


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_id', 'first_name', 'last_name', 'date_of_birth']
        widgets = {
            'patient_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control'})
        }


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['rx_id', 'name', 'dosage', 'appointment_days_needed']
        widgets = {
            'rx_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.NumberInput(attrs={'class': 'form-control'}),
            'appointment_days_needed': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'refill_date_display', 'days_dispensed', 'last_refill_date']