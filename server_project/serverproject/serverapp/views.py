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
from asgiref.sync import sync_to_async
from .signals import trainingStrated
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

MODEL_DIR = "..\serverproject\client_files"


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
    clients = clients.filter(status="Active")
    return clients

async def startRound(request):
    clients = await sync_to_async(select_clients())
    try:
        for client in clients:
            client_url = f"http://{client.ip}:{client.port}/start_training/"
            response = await requests.post(client_url, data={"message":"Start training model"}, timeout=10)
            if response.status_code == 500:
                client.status = "Inactive"
                await sync_to_async(ClientInfo.save(client))
            elif response.status_code == 200:
                continue
        trainingStrated.asend(sender = None)
    except Exception as e:
        print(e)

@csrf_exempt
async def RecieveFiles(request):
    if request.method == "POST":
        try:
            client = await sync_to_async(ClientInfo.objects.get)(name=request.POST.get("name"))
            path = os.path.join(MODEL_DIR, client.name)
            file = request.FILES.get("file")
            with open(path, 'wb') as f:
                content = file.read()
                f.write(content)
            client.model_file = path
            await sync_to_async(client.save)()
            return JsonResponse({"saved_file":"successfilly"}, status=200)
        except Exception as e:
            return JsonResponse({"Error":f"Error saving client. {e}"}, status = 500)
    else:
        return JsonResponse({"Error":"Method not allowed"}, status = 500)

    

    



























'''
# try:
        #     client_id = request.POST.get("id")
        #     client = sync_to_async(ClientInfo.objects.get)(id=client_id)
        #     file = request.FILES.get("file")
        #     client.model_file = file
        #     asyncio.to_thread(client.save())
        #     return Response({"message":"file saved successfully."}, status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"message":e+"Cannot save file"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


# async def recieve_models(request):
#     if request.method == "POST":
#         try:
#             client_id = request.POST.get("id")
#             client = sync_to_async(ClientInfo.objects.get(id=client_id))
#             if 'file' in request.FILES:
#                 file = request.FILES['file']
#                 client.model_file = file
#                 asyncio.to_thread(client.save())
#                 return Response({"message":"File saved successfully."}, status.HTTP_200_OK)
#             else:
#                 return Response({"message":"File not found."}, status.HTTP_410_GONE)
#         except Exception as e:
#             print(e)
#             return Response({"message":"e. Faield to save file."},status.HTTP_500_INTERNAL_SERVER_ERROR)


    
    parser_classes = [FormParser, MultiPartParser]
    def put(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        try:
            client_instance = ClientInfo.objects.get(id = client_id)
        except ClientInfo.DoesNotExist:
            return Response({'error': 'ClientInfo not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FileExistsError(instance = client_instance, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''


        