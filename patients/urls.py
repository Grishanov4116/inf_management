# patients/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Общие страницы
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    
    # Пациенты
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/add/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    
    # Медицинские записи
    path('patients/<int:patient_id>/records/add/', views.medical_record_create, name='medical_record_create'),
    
    # Приемы
    path('patients/<int:patient_id>/appointments/add/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/status/<str:status>/', views.appointment_update_status, name='appointment_update_status'),
    
    # Телемедицина
    path('patients/<int:patient_id>/telemedicine/add/', views.telemedicine_create, name='telemedicine_create'),
    path('telemedicine/<int:pk>/start/', views.telemedicine_start, name='telemedicine_start'),
    path('telemedicine/<int:pk>/', views.telemedicine_session, name='telemedicine_session'),
]