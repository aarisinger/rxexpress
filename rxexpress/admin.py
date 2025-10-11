from django.contrib import admin

from .models import Patient, Medication, Prescription


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ('patient_id', 'first_name', 'last_name', 'date_of_birth')


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
	list_display = ('rx_id', 'name', 'dosage', 'appointment_days_needed')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
	list_display = ('patient', 'medication', 'last_refill_date', 'last_appointment_date')
