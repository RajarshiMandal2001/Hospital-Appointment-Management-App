from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from hospital.models import Appointment
from hospital.serializers.appointment_serializer import AppointmentSerializer, AppointmentCreateSerializer
from rest_framework.decorators import api_view, permission_classes

# class based end point
class AppointmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # serializer = AppointmentSerializer(data=request.data)
        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# function based end point
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_appointments_by_patient(request, patient_id):
    try:
        appointments = Appointment.objects.filter(patient_id=patient_id)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Something went wrong or patient not found'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_appointments_by_doctor(request, doctor_id):
    try:
        appointments = Appointment.objects.filter(doctor_id=doctor_id)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Something went wrong or doctor not found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_appointment_date(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        new_date = request.data.get('date_appointment')

        if not new_date:
            return Response({'error': 'Missing date_appointment field'}, status=status.HTTP_400_BAD_REQUEST)

        appointment.date_appointment = new_date
        appointment.save()

        return Response({'message': 'Appointment date updated successfully'}, status=status.HTTP_200_OK)
    
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_appointment_by_id(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.delete()
        return Response({'message': 'Appointment deleted successfully.'}, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
