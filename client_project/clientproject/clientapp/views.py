from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .signals import data_loaded, start_training, training_finished
# Create your views here.
import requests
SERVER_URL = 'http://127.0.0.1:8000'
    
def registerToServer(sender, *args, **kwargs):
    print("Registering to server.")
    endpoint = f"{SERVER_URL}/register/"
    data = {
        "name":"CLIENT001",
        "ip": "192.168.123.132",
        "port": 8000
    }
    try:
        response = requests.post(endpoint, data=data)
        print("Successfull Registeration Response:", response.json())
    except Exception as e:
        print(f'Failed to register client. Response: {e}')

data_loaded.connect(registerToServer)


def tell_server_training_finished(*args, **kwargs):
    endpoint = f'{SERVER_URL}/client_training_status'
    data = {
        "message": "Client Training Finished",
    }
    try:
        response = requests.post(endpoint, data=data)
        print("Successfilly informed server training status:", response.json())
    except Exception as e:
        print(f'Failed to register client. Response:{e}')
    
training_finished.connect(tell_server_training_finished)



class StartTrainingView(APIView):
    """
    Sends a signal after reciving message from server that round has begun. 
    The signal is consumed by helper functions to load data train model and save the model file. 
    """
    def post(self, request, *args, **kwargs):
        start_training.send(sender=self.__class__)
        return Response({"message": "Started loading data."}, status=status.HTTP_200_OK)

