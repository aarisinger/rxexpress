from django import forms
from .models import Patient, Prescription, Medication


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'last_appointment', 'patient_id']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name', 'size': 40}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name', 'size': 40}),
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY', 'type': 'date'}),
            'last_appointment': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY', 'type': 'date'}),
            'patient_id': forms.TextInput(attrs={'placeholder': 'Last Name + DOB(MMDDYYYY)', 'size': 40})
        }


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['rx_id', 'name', 'dosage', 'appointment_days_needed']
        widgets = {
            'rx_id': forms.TextInput(attrs={'placeholder': 'Enter Medication Name + Dosage', 'size': 40}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Medication Name', 'size': 40}),
            'dosage': forms.NumberInput(attrs={'placeholder': 'Enter Dosage Amount'}),
            'appointment_days_needed': forms.NumberInput(attrs={'placeholder': 'Days req. for follow up'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'days_dispensed', 'last_refill_date']
