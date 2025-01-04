import os
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ClientInfoSerializer, FileUploadSerialiser
from rest_framework import status
from rest_framework.decorators import APIView, api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from .models import ClientInfo
from django.core.files import File
import requests
import asyncio
from .utils import ClientsRoundManager
from asgiref.sync import sync_to_async
from .signals import trainingStrated
from django.views.decorators.csrf import csrf_exempt
from .utils import aggregate_client_files, create_and_save_model
# Create your views here.

MODEL_DIR = "..\serverproject\client_files"

num_client_files_recieved = 0

# instead of having signals have a parent function calling all the functions one after another.
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
    
def select_clients():
    clients = ClientInfo.objects.all()
    # clients = clients.filter(status="Active")
    return clients

async def startRound():
    """
    Start rounds. 
    Select clients and send them requests to start training. 
    Depending on response consider client active or inactive for current round. 
    """
    path = "serverproject\server_model\servermodel.h5"
    create_and_save_model(path=path)
    clients = await sync_to_async(select_clients())
    selected_clients = []
    try:
        for client in clients:
            client_url = f"http://{client.ip}:{client.port}/start_training/"
            files = {"file":(open(path, "rb"))}
            response = await requests.post(client_url, data={"message":"Start training model"}, timeout=10)
            if response.status_code == 500:
                client.status = "Inactive"
                await sync_to_async(ClientInfo.save(client))
            elif response.status_code == 200:
                select_clients.append(client)
                continue
        """Signal recieved by utility class that keeps a track of clients included in server."""
    except Exception as e:
        print(e)    
    return selected_clients

@csrf_exempt
async def RecieveFiles(request):
    """Client will send files here after completing training."""
    if request.method == "POST":
        try:
            client = await sync_to_async(ClientInfo.objects.get)(name=request.POST.get("name"))
            path = os.path.join(MODEL_DIR, client.name, ".h5")
            file = request.FILES.get("file")
            with open(path, 'wb') as f:
                content = file.read()#maybe in chunks if this doesnt work. 
                
                f.write(content)
            client.model_file = path
            await sync_to_async(client.save)()
            return JsonResponse({"saved_file":"successfilly"}, status=200)
        except Exception as e:
            return JsonResponse({"Error":f"Error saving client. {e}"}, status = 500)
    else:
        return JsonResponse({"Error":"Method not allowed"}, status = 500)
    

async def broadCastFiles(selected_clients:list, path:str):
    responses = []
    try:
        for client in selected_clients:
            client_url = f"http://{client.ip}:{client.port}/aggregated_file/"
            file = open(path, "rb")
            response = await requests.post(client_url,data={"message":"aggregated model"} ,files={"file":file})
            responses.append((response, client.name))
            print(response)
    except Exception as e: 
        print("Error in fucntion broadcastFiles",e)
    return responses



async def RoundManager(request):
    num_client_files_recieved = 0
    selected_clients = await startRound()#function to start rounds returns list of clients that accepted message and started training.
    for i in request.data.get("epochs"):
        num_client_files_recieved = 0
        total_clients = len(select_clients)
        try:
            await asyncio.wait_for( wait_for_files(total_clients), timeout=50 )
        #Considering nothing goes wrong, wait till all clients send files. 
        except asyncio.TimeoutError:
            print("Timed out. Not all clients sent their files. ")
        broadcast_path = sync_to_async(aggregate_client_files)(select_clients)#function to aggregate client models and broadcast. 
        responses = await broadCastFiles()
        print(responses)
    num_client_files_recieved = 0


async def wait_for_files(total_clients):
    while num_client_files_recieved<total_clients:
        await asyncio.sleep(1)
        print("All files recieved")