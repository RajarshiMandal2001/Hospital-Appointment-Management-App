from django.urls import path
from hospital.views.doctor_views import *
from hospital.views.patient_views import *
from hospital.views.appointment_views import *
from hospital.views.appointment_views import (
    get_appointments_by_patient, get_appointments_by_doctor, delete_appointment_by_id, update_appointment_date
)
from hospital.views.auth_views import LogoutView

urlpatterns = [
    # Doctor endpoints
    path('doctors/register/', DoctorRegisterView.as_view()),
    path('doctors/login/', DoctorLoginView.as_view()),
    path('doctors/', DoctorListCreateView.as_view()),

    # Patient endpoints
    path('patients/register/', PatientRegisterView.as_view()),
    path('patients/login/', PatientLoginView.as_view()),
    path('patients/', PatientListCreateView.as_view()),

    # Appointment endpoints
    path('appointments/', AppointmentListCreateView.as_view()),
    path('appointments/<int:patient_id>/', get_appointments_by_patient, name='appointments-by-patient'),
    path('appointments/doctor/<int:doctor_id>/', get_appointments_by_doctor, name='appointments-by-doctor'),
    path('appointments/update/<int:appointment_id>/', update_appointment_date, name='update-appointment-date'),
    path('appointments/delete/<int:appointment_id>/', delete_appointment_by_id, name='delete-appointment-by-id'),


    path('logout/', LogoutView.as_view(), name='logout'),
]
