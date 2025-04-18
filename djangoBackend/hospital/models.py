from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    fees = models.IntegerField()
    specialist = models.CharField(max_length=10, choices=[('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3')])

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_booking = models.DateTimeField(auto_now_add=True)
    date_appointment = models.DateTimeField()

    def __str__(self):
        return f"{self.patient.user.username} with {self.doctor.user.username}"
