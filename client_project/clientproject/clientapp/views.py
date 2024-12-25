from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from asgiref.sync import sync_to_async
from .utils import data_loaded
from .signals import start_training, training_finished
# Create your views here.
import requests
SERVER_URL = 'http://127.0.0.1:8000'
    
def registerToServer(sender, *args, **kwargs):
    print("Registering to server.", sender)
    endpoint = f"{SERVER_URL}/register/"
    data = {
        "name":"CLIENT001",
        "ip": "192.168.123.132",
        "port": 8000
    }
    try:
        print(f"Attempting to register with endpoint: {endpoint}")
        print(f"Registration data: {data}")
        response = requests.post(endpoint, json=data)
        
        # Print full response details for debugging
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        try:
            print(f"Response Content: {response.text}")
        except Exception as content_error:
            print(f"Could not print response content: {content_error}")
        
        response.raise_for_status()
        print("Successful Registration Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Failed to register client. Error: {e}")
        # Add more detailed error information
        import traceback
        traceback.print_exc()

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
        try:
            start_training.send(sender=self.__class__)
            return Response({"message": "Started loading data."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"Can't train.", "error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
async def RecieveFiles(request):
    if request.method == "POST":
        try:
            client = await sync_to_async(Client.objects.get)(name=request.POST.get("name"))
            path = os.path.join(MODEL_DIR, client.name)
            file = request.FILES.get("file")
            with open(path, 'wb') as f:
                content = file.read()
                f.write(content)
            client.filepath = path
            await sync_to_async(client.save)()
            return JsonResponse({"saved_file":"successfilly"}, status=200)
        except Exception as e:
            return JsonResponse({"Error":f"Error saving client. {e}"}, status = 500)
    else:
        return JsonResponse({"Error":"Method not allowed"}, status = 500)

