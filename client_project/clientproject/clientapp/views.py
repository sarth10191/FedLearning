from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from asgiref.sync import sync_to_async
from .utils import data_loaded
from .signals import start_training, training_finished
# Create your views here.
from django.http import JsonResponse
import requests
SERVER_URL = 'http://127.0.0.1:8000'
    
def registerToServer(sender, *args, **kwargs):
    print("Registering to server.", sender)
    endpoint = f"{SERVER_URL}/register/"
    data = {
        "name":"CLIENT001",
        "ip": "127.0.0.1",
        "port": 8001
    }
    try:
        print(f"Attempting to register with endpoint: {endpoint}")
        print(f"Registration data: {data}")
        response = requests.post(endpoint, json=data)
        
        # Print full response details for debugging
        print(f"Response Status Code: {response.status_code}")
        print("Successful Registration Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Failed to register client. Error: {e}")
        # Add more detailed error information
        
data_loaded.connect(registerToServer)

def send_files_to_server(*args, **kwargs):
    endpoint = f'{SERVER_URL}/client_training_status'
    path = "path to .h5 file saved by client"
    data = {
        "name": "CLIENT001",
    }
    files = {"file":(open(path, "rb"))}
    try:
        response = requests.post(endpoint, data=data, files=files)
        print("Successfilly informed server training status:", response.json())
    except Exception as e:
        print(f'Failed to register client. Response:{e}')
    
training_finished.connect(send_files_to_server)



class StartTrainingView(APIView):
    """
    Sends a signal after reciving message from server that round has begun. 
    The signal is consumed by helper functions to load data train model and save the model file. 
    """
    def post(self, request, *args, **kwargs):
        path = "clientproject/my_model/my_model.h5"
        try:
            file = request.FILES.get("file")
            with open(path, "rb") as myfile:
                content = file.read()
                myfile.write(content)
            start_training.send(sender=self.__class__, path = path)
            return Response({"message": "Started loading data."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"Can't train.", "error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        