from django.db import models
from datetime import date, timedelta

# Models aligned to the Excel workbook
class Patient(models.Model):
    # Excel column: 'Patient ID'
    patient_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # Excel column: 'Date of Birth' (stored as date)
    date_of_birth = models.DateField(null=True, blank=True)
    # These two are present per-row in the patient sheet (last appointment/refill)
    last_appointment = models.DateField(null=True, blank=True)
    last_fill_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient_id} {self.first_name} {self.last_name}"


class Medication(models.Model):
    # Excel sheet 'drug' -> 'Rx ID'
    rx_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    # store dosage as numeric when possible
    dosage = models.FloatField(null=True, blank=True)
    # Excel column 'Appointment days needed'
    appointment_days_needed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.rx_id} {self.name} {self.dosage or ''}"


class Prescription(models.Model):
    # Links a patient to a medication and stores refill/appointment metadata
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions', null=True, blank=True)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='prescriptions', null=True, blank=True)

    # Excel patient sheet columns
    refill_date_display = models.CharField(max_length=100, null=True, blank=True)
    days_dispensed = models.IntegerField(null=True, blank=True)
    last_refill_date = models.DateField(null=True, blank=True)
    days_since_last_refill = models.IntegerField(null=True, blank=True)
    appointment_date_display = models.CharField(max_length=100, null=True, blank=True)
    last_appointment_date = models.DateField(null=True, blank=True)
    days_since_last_appointment = models.IntegerField(null=True, blank=True)
    appointment_date_requirement = models.IntegerField(null=True, blank=True)

    # original Rx ID from Excel (redundant but useful)
    rx_id = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('patient', 'medication')

    def __str__(self):
        return f"{self.patient.patient_id} - {self.medication.rx_id}"
    
    @property
    def days_since_last_refill(self):
        if not self.last_refill_date:
            return None
        return (date.today() - self.last_refill_date).days
    
    @property
    def refill_ready(self):
        if self.days_since_last_refill is None or self.days_dispensed is None:
            return False
        return self.days_since_last_refill >=(self.days_dispensed - 5)
    
    @property
    def appointment_ok(self):
        last_appt = self.last_appointment_date or(
            self.patient.last_appointment if self.patient else None
        )
        if not last_appt or not self.medication or not self.medication.appointment_days_needed:
            return False
        days_since_appointment = (date.today() - last_appt).days
        return days_since_appointment <= self.medication.appointment_days_needed
    
    @property
    def eligible_for_refill(self):
        return self.refill_ready and self.appointment_ok
    
    def __str__(self):
        return f"Prescription for {self.patient} - {self.medication}"