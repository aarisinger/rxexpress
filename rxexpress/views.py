from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Prescription, Medication
from .forms import PatientForm, PrescriptionForm, MedicationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    sentence = 'Welcome to RxExpress Refill Tracker!'
    return render(request, 'index.html', {'sentence': sentence})


def patient_form_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})


def prescription_form_view(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PrescriptionForm()
    return render(request, 'add_prescription.html', {'form': form})


def medication_form_view(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MedicationForm()
    return render(request, 'add_medication.html', {'form': form})


@login_required
def dashboard(request):
    patients_count = Patient.objects.count()
    medications_count = Medication.objects.count()
    prescriptions_count = Prescription.objects.count()

    q = request.GET.get('q', '').strip()
    prescriptions = None
    patient_results = None
    if q:
        # lookup by patient_id or name
        patient_results = Patient.objects.filter(patient_id__icontains=q) | Patient.objects.filter(first_name__icontains=q) | Patient.objects.filter(last_name__icontains=q)
        prescriptions = Prescription.objects.filter(patient__in=patient_results).select_related('medication', 'patient')

    return render(request, 'dashboard.html', {
        'patients_count': patients_count,
        'medications_count': medications_count,
        'prescriptions_count': prescriptions_count,
        'query': q,
        'prescriptions': prescriptions,
    })


@login_required
def patient_list_view(request):
    patients = Patient.objects.all().order_by('last_name', 'first_name')
    return render(request, 'patient_list.html', {'patients': patients})


@login_required
def patient_detail_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    prescriptions = patient.prescriptions.select_related('medication')
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_detail.html', {'patient': patient, 'form': form, 'prescriptions': prescriptions})


@login_required
def patient_delete_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patient_confirm_delete.html', {'patient': patient})
