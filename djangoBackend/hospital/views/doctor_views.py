from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from hospital.models import Doctor
from hospital.serializers.doctor_serializer import DoctorSerializer, DoctorRegisterSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class DoctorRegisterView(APIView):
    def post(self, request):
        serializer = DoctorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Doctor registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user and hasattr(user, 'doctor'):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'id': user.doctor.id 
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class DoctorListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     doctors = Doctor.objects.all()
    #     serializer = DoctorSerializer(doctors, many=True)
    #     return Response(serializer.data)

    def get(self, request):
        name = request.query_params.get('name', None)
        if name:
            doctors = Doctor.objects.filter(user__username__icontains=name)
        else:
            doctors = Doctor.objects.all()

        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = DoctorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
