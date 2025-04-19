from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import Patient, MedicalRecord, Appointment, TelemedicineSession
from .forms import PatientForm, MedicalRecordForm, AppointmentForm, TelemedicineSessionForm, SessionSummaryForm

@login_required
def dashboard(request):
    """Главная страница с основной статистикой и ближайшими событиями"""
    today = timezone.now().date()
    
    # Статистика
    patient_count = Patient.objects.count()
    appointments_today = Appointment.objects.filter(date_time__date=today).count()
    telemedicine_today = TelemedicineSession.objects.filter(scheduled_time__date=today).count()
    
    # Ближайшие приемы
    upcoming_appointments = Appointment.objects.filter(
        status='SCHEDULED',
        date_time__gte=timezone.now()
    ).order_by('date_time')[:5]
    
    # Телемедицинские консультации на сегодня
    today_sessions = TelemedicineSession.objects.filter(
        scheduled_time__date=today
    ).order_by('scheduled_time')

    context = {
        'patient_count': patient_count,
        'appointments_today': appointments_today,
        'telemedicine_today': telemedicine_today,
        'upcoming_appointments': upcoming_appointments,
        'today_sessions': today_sessions,
    }
    
    return render(request, 'patients/dashboard.html', context)

@login_required
def patient_list(request):
    """Список пациентов с возможностью поиска"""
    search_query = request.GET.get('search', '')
    
    if search_query:
        patients = Patient.objects.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(medical_insurance_number__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    else:
        patients = Patient.objects.all()
    
    context = {
        'patients': patients,
        'search_query': search_query
    }
    
    return render(request, 'patients/patient_list.html', context)

@login_required
def patient_detail(request, pk):
    """Детальная информация о пациенте, включая мед. записи и приемы"""
    patient = get_object_or_404(Patient, pk=pk)
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')
    telemedicine_sessions = TelemedicineSession.objects.filter(patient=patient).order_by('-scheduled_time')
    
    context = {
        'patient': patient,
        'medical_records': medical_records,
        'appointments': appointments,
        'telemedicine_sessions': telemedicine_sessions,
    }
    
    return render(request, 'patients/patient_detail.html', context)

@login_required
def patient_create(request):
    """Создание нового пациента"""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            messages.success(request, 'Пациент успешно добавлен.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required
def patient_update(request, pk):
    """Редактирование данных пациента"""
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные пациента обновлены.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/patient_form.html', {'form': form, 'patient': patient})

@login_required
def patient_delete(request, pk):
    """Удаление пациента"""
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Пациент удален.')
        return redirect('patient_list')
    
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})

@login_required
def medical_record_create(request, patient_id):
    """Создание медицинской записи для пациента"""
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.doctor = request.user
            record.save()
            messages.success(request, 'Медицинская запись добавлена.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = MedicalRecordForm()
    
    return render(request, 'patients/medical_record_form.html', {
        'form': form,
        'patient': patient
    })

@login_required
def appointment_create(request, patient_id):
    """Создание записи на прием для пациента"""
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, 'Запись на прием создана.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = AppointmentForm()
    
    return render(request, 'patients/appointment_form.html', {
        'form': form,
        'patient': patient
    })

@login_required
def appointment_update_status(request, pk, status):
    """Обновление статуса приема (завершен, отменен)"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if status in ['COMPLETED', 'CANCELED']:
        appointment.status = status
        appointment.save()
        status_text = 'завершен' if status == 'COMPLETED' else 'отменен'
        messages.success(request, f'Прием {status_text}.')
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def telemedicine_create(request, patient_id):
    """Создание телемедицинской консультации для пациента"""
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        form = TelemedicineSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.patient = patient
            session.save()
            messages.success(request, 'Телемедицинская консультация запланирована.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = TelemedicineSessionForm()
    
    return render(request, 'patients/telemedicine_form.html', {
        'form': form,
        'patient': patient
    })

@login_required
def telemedicine_start(request, pk):
    """Начало телемедицинской консультации"""
    session = get_object_or_404(TelemedicineSession, pk=pk)
    
    if session.status == 'SCHEDULED':
        session.status = 'IN_PROGRESS'
        session.actual_start_time = timezone.now()
        session.save()
        messages.success(request, 'Телемедицинская консультация начата.')
    
    return redirect('telemedicine_session', pk=session.pk)

@login_required
def telemedicine_session(request, pk):
    """Страница текущей телемедицинской консультации"""
    session = get_object_or_404(TelemedicineSession, pk=pk)
    
    if request.method == 'POST' and session.status == 'IN_PROGRESS':
        form = SessionSummaryForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.actual_end_time = timezone.now()
            session.status = 'COMPLETED'
            session.save()
            messages.success(request, 'Телемедицинская консультация завершена.')
            return redirect('patient_detail', pk=session.patient.pk)
    else:
        form = SessionSummaryForm(instance=session)
    
    return render(request, 'patients/telemedicine_session.html', {
        'session': session,
        'form': form
    })