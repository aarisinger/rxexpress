# Auto-generated initial migration replaced to match current models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=50, null=True, blank=True, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('last_appointment', models.DateField(blank=True, null=True)),
                ('last_fill_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rx_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('dosage', models.FloatField(blank=True, null=True)),
                ('appointment_days_needed', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refill_date_display', models.CharField(max_length=100, null=True, blank=True)),
                ('days_dispensed', models.IntegerField(null=True, blank=True)),
                ('last_refill_date', models.DateField(null=True, blank=True)),
                ('days_since_last_refill', models.IntegerField(null=True, blank=True)),
                ('appointment_date_display', models.CharField(max_length=100, null=True, blank=True)),
                ('last_appointment_date', models.DateField(null=True, blank=True)),
                ('days_since_last_appointment', models.IntegerField(null=True, blank=True)),
                ('appointment_date_requirement', models.IntegerField(null=True, blank=True)),
                ('rx_id', models.CharField(max_length=50, null=True, blank=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, related_name='prescriptions', to='rxexpress.patient')),
                ('medication', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, related_name='prescriptions', to='rxexpress.medication')),
            ],
            options={
                'unique_together': {('patient', 'medication')},
            },
        ),
    ]
