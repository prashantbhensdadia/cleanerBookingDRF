from base.models import *
from django.db import transaction
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes

# Create new user view
class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            if not request.data:
                # Retrun error message with 400 status
                return Response({"message": "Data is required.", "status": status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
            
            phone_no = request.data.get('phone_no')
            password = request.data.get('password')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            city = request.data.get('city')
            time = request.data.get('time')
            
            if not phone_no:
                # Retrun error message with 400 status
                return Response({"message": "Phone no is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
            
            if not password:
                # Retrun error message with 400 status
                return Response({"message": "Password is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)                                
            
            if len(phone_no) > 10 or len(phone_no) < 10:
                # Retrun error message with 400 status
                return Response({"message": "Phone no should be 10 digits.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST) 

            # Generating an unique token for each user
            user = User.objects.filter(phone_no = phone_no).first()
            if not user:
                if not first_name:
                    # Retrun error message with 400 status
                    return Response({"message": "First name is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
            
                if not last_name:
                    # Retrun error message with 400 status
                    return Response({"message": "Last name is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

                if not city:
                    # Retrun error message with 400 status
                    return Response({"message": "City is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

                if not time:
                    # Retrun error message with 400 status
                    return Response({"message": "Date and time is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)    
                
                city_obj = City.objects.filter(id = city).first()
            
                if not city_obj:
                    return Response({"message": "City is not found.", "status":status.HTTP_404_NOT_FOUND}, status.HTTP_404_NOT_FOUND)
                
                user = User(
                                phone_no= phone_no
                                )
                user.set_password(password)
            
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            
            cleaners = Cleaner.objects.filter(city = city)
            busy_cleaners = Appointment.objects.filter(time = time).values_list('cleaner_id', flat = True)
            available_cleaners = []
            
            for cleaner in cleaners:
                if cleaner.id not in busy_cleaners:
                    available_cleaners.append(cleaner)
        
            if available_cleaners:
                appointment = Appointment.objects.create(user= user, cleaner= available_cleaners[0], time = time)  
                data = appointment.cleaner.first_name + " " +  appointment.cleaner.last_name       
                return Response({"message": "This cleaner is booked for an appointment.", "data": data,
                                            "status": status.HTTP_200_OK}, status.HTTP_200_OK)
            
            return Response({"message": "No cleaner found for given time", "status": status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)                                            


class GetCityList(APIView):
    
    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        data = []
        for city in cities:
            data.append({
                'id': city.id,
                'name':city.name
            })
        
        response = {}
        response['status'] = status.HTTP_200_OK
        response['message'] = "Followinf cities are found."
        response['data'] = data
        
        return Response(response, status = status.HTTP_200_OK)


class CleanerCreateView(CreateAPIView):
    serializer_class = CleanerCreateSerializer

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            if not request.data:
                # Retrun error message with 400 status
                return Response({"message": "Data is required.", "status": status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            city = request.data.get('city')
            
            if not first_name:
                # Retrun error message with 400 status
                return Response({"message": "First name is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
            
            if not last_name:
                # Retrun error message with 400 status
                return Response({"message": "Last name is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

            if not city:
                # Retrun error message with 400 status
                return Response({"message": "City is required.", "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)                                

            serializer = self.get_serializer(data=request.data)
            
            # check validation of serializer data
            if not serializer.is_valid(raise_exception=False):
                error_msg = serializer.errors
                if serializer.errors.get('city'):
                    error_msg = 'City does not exist.'                                               

                # Retrun error message with 400 status
                return Response({"message": error_msg,"status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

            self.perform_create(serializer)
            
            return Response({"message": "User is created successfully.", "data": serializer.data,
                                        "status": status.HTTP_201_CREATED}, status.HTTP_201_CREATED)

    # saves user in database
    def perform_create(self, serializer):
        serializer.save()