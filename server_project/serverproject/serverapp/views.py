from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ClientInfoSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import ClientInfo
from .signals import start_training
from .utils import load_data
# Create your views here.
class RegisterClientView(APIView):
    """
    Handle clinet registeration.
    """
    def post(self, request, *args, **kwargs):
        serializer = ClientInfoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Client registered Successfully.", "client_name":serializer.data['name']},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StartTrainingView(APIView):
    """
    Sends a signal after reciving message from server that round has begun. 
    The signal is consumed by helper functions to load data train model and save the model file. 
    """
    def post(self, request, *args, **kwargs):
        start_training.send(sender=self.__class__)
        return Response({"message": "Started loading data."}, status=status.HTTP_200_OK)

        

class DeregisterClientView(APIView):
    """
    Handle client deregisterations.
    """
    def post(request):
        client_id = request.data.get('name')
        try:
            client = ClientInfo.objects.get(id = client_id)
            client.status = ClientInfo.StatusChoices.DEREGISTERED
            client.save()
            return Response(
                {"message":"Client Deregistered Successfully",},
                status= status.HTTP_200_OK
            )
        except ClientInfo.DoesNotExist:
            return Response({"error":"Client not found."}, 
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":e})
        

