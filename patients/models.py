from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    date_of_birth = models.DateField('Дата рождения')
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField('Телефон', max_length=15)
    address = models.TextField('Адрес')
    medical_insurance_number = models.CharField('Номер полиса ОМС', max_length=16, unique=True)
    allergies = models.TextField('Аллергии', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_records')
    diagnosis = models.CharField('Диагноз', max_length=255)
    symptoms = models.TextField('Симптомы')
    treatment = models.TextField('Лечение')
    notes = models.TextField('Примечания', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Медицинская запись'
        verbose_name_plural = 'Медицинские записи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Запись {self.id} для пациента {self.patient}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Запланирован'),
        ('COMPLETED', 'Завершен'),
        ('CANCELED', 'Отменен'),
        ('RESCHEDULED', 'Перенесен'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    date_time = models.DateTimeField('Дата и время')
    reason = models.TextField('Причина обращения')
    status = models.CharField('Статус', max_length=15, choices=STATUS_CHOICES, default='SCHEDULED')
    notes = models.TextField('Примечания', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Прием'
        verbose_name_plural = 'Приемы'
        ordering = ['-date_time']
    
    def __str__(self):
        return f"Прием {self.patient} у {self.doctor.last_name} {self.doctor.first_name} - {self.date_time}"


class TelemedicineSession(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Запланирована'),
        ('IN_PROGRESS', 'В процессе'),
        ('COMPLETED', 'Завершена'),
        ('CANCELED', 'Отменена')
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='telemedicine_sessions')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_telemedicine_sessions')
    scheduled_time = models.DateTimeField('Запланированное время')
    actual_start_time = models.DateTimeField('Фактическое время начала', null=True, blank=True)
    actual_end_time = models.DateTimeField('Фактическое время окончания', null=True, blank=True)
    status = models.CharField('Статус', max_length=15, choices=STATUS_CHOICES, default='SCHEDULED')
    complaint = models.TextField('Жалоба')
    summary = models.TextField('Заключение', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Телемедицинская консультация'
        verbose_name_plural = 'Телемедицинские консультации'
        ordering = ['-scheduled_time']
    
    def __str__(self):
        return f"Телемедицинская консультация: {self.patient} - {self.doctor.last_name} {self.doctor.first_name}"