from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
from rxexpress.models import Patient, Medication, Prescription
from django.db import transaction


class Command(BaseCommand):
    help = 'Import patients and drugs from the Excel outline of databases.xlsx'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default='Excel outline of databases.xlsx')

    def handle(self, *args, **options):
        path = Path(options['path'])
        if not path.exists():
            self.stderr.write(f'File not found: {path}')
            return

        xl = pd.ExcelFile(path)

        # Import drugs first (sheet named 'drug')
        if 'drug' in xl.sheet_names:
            df_drug = xl.parse('drug')
            self.stdout.write(f'Importing {len(df_drug)} drugs')
            for _, row in df_drug.iterrows():
                rx_id = str(row.get('Rx ID')).strip()
                name = row.get('Rx name')
                dosage = row.get('Rx dosage')
                appointment_days_needed = row.get('Appointment days needed')
                if rx_id == 'nan' or not rx_id:
                    continue
                med, _ = Medication.objects.update_or_create(
                    rx_id=rx_id,
                    defaults={
                        'name': name,
                        'dosage': float(dosage) if pd.notna(dosage) else None,
                        'appointment_days_needed': int(appointment_days_needed) if pd.notna(appointment_days_needed) else None,
                    }
                )

        # Import patients and prescriptions
        if 'patient' in xl.sheet_names:
            df_pat = xl.parse('patient')
            self.stdout.write(f'Importing {len(df_pat)} patient rows')
            for _, row in df_pat.iterrows():
                patient_id = str(row.get('Patient ID')).strip()
                first_name = row.get('First Name')
                last_name = row.get('Last Name')
                dob = row.get('Date of Birth')
                rx_id = str(row.get('Rx ID')).strip()
                rx_name = row.get('Rx Name')
                rx_dosage = row.get('Rx Dosage')

                if patient_id == 'nan' or not patient_id:
                    continue

                last_appointment = row.get('Last appointment date')
                last_fill_date = row.get('Last refill date')

                patient_obj, _ = Patient.objects.update_or_create(
                    patient_id=patient_id,
                    defaults={
                        'first_name': first_name or '',
                        'last_name': last_name or '',
                        'date_of_birth': pd.to_datetime(dob, errors='coerce').date() if pd.notna(dob) else None,
                        'last_appointment': pd.to_datetime(last_appointment, errors='coerce').date() if pd.notna(last_appointment) else None,
                        'last_fill_date': pd.to_datetime(last_fill_date, errors='coerce').date() if pd.notna(last_fill_date) else None,
                    }
                )

                # find or create medication by rx_id or name
                med = None
                if rx_id and rx_id != 'nan':
                    med = Medication.objects.filter(rx_id=rx_id).first()
                if med is None and rx_name:
                    med = Medication.objects.filter(name=str(rx_name)).first()
                if med is None:
                    med = Medication.objects.create(
                        rx_id=rx_id or f'RX-{patient_id}-{rx_name}',
                        name=rx_name or '',
                        dosage=float(rx_dosage) if pd.notna(rx_dosage) else None,
                    )

                # create or update prescription
                last_refill_date = row.get('Last refill date')
                last_appointment_date = row.get('Last appointment date')

                if last_appointment_date and not patient_obj.last_appointment:
                    patient_obj.last_appointment = pd.to_datetime(last_appointment_date, errors='coerce').date()
                    patient_obj.save()
                

                Prescription.objects.update_or_create(
                    patient=patient_obj,
                    medication=med,
                    defaults={
                        'refill_date_display': row.get('Refill Date Display') or '',
                        'days_dispensed': int(row.get('# of days dispensed')) if pd.notna(row.get('# of days dispensed')) else None,
                        'last_refill_date': pd.to_datetime(last_refill_date, errors='coerce').date() if pd.notna(last_refill_date) else None,
                        'days_since_last_refill': int(row.get('# Days since last refill')) if pd.notna(row.get('# Days since last refill')) else None,
                        'appointment_date_display': row.get('Appointment Date Display') or '',
                        'last_appointment_date': pd.to_datetime(last_appointment_date, errors='coerce').date() if pd.notna(last_appointment_date) else None,
                        'days_since_last_appointment': int(row.get('Days since last appointment')) if pd.notna(row.get('Days since last appointment')) else None,
                        'appointment_date_requirement': int(row.get('Appointment date requirement')) if pd.notna(row.get('Appointment date requirement')) else None,
                        'rx_id': rx_id or None,
                    }
                )

        self.stdout.write('Import complete')