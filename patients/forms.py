from django import forms
from .models import Patient, MedicalRecord, Appointment, TelemedicineSession
from django.contrib.auth.models import User

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 
                  'address', 'medical_insurance_number', 'allergies']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'symptoms', 'treatment', 'notes']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason', 'status', 'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Фильтруем докторов (предполагается, что у докторов есть определенная группа или права)
        self.fields['doctor'].queryset = User.objects.filter(is_staff=True)


class TelemedicineSessionForm(forms.ModelForm):
    class Meta:
        model = TelemedicineSession
        fields = ['doctor', 'scheduled_time', 'complaint', 'status']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'complaint': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(TelemedicineSessionForm, self).__init__(*args, **kwargs)
        # Фильтруем докторов
        self.fields['doctor'].queryset = User.objects.filter(is_staff=True)


class SessionSummaryForm(forms.ModelForm):
    class Meta:
        model = TelemedicineSession
        fields = ['summary', 'status']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 5}),
        }