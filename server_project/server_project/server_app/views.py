# import requests
# from django.http import JsonResponse
# from .models import Client
# from rest_framework.response import Response
# import os

# def request_training_from_client(request):
#     clients = Client.objects.all()
#     responses = {}
    
#     for client in clients:
#         client_url = f"http://{client.host}:{client.port}/client/train-and-send/"

#         try:
#             # Request to trigger training on client-side
#             response = requests.get(client_url)
#             responses[client.user.username] = response.json()

#         except requests.exceptions.RequestException as e:
#             responses[client.user.username] = {"error": str(e)}

#     return JsonResponse(responses)


# def receive_model(request):
#     if request.method == "POST":
#         model_file = request.FILES.get('model')
#         summary_file = request.FILES.get('summary')

#         # Directory to save files
#         os.makedirs("received_files", exist_ok=True)
#         model_path = os.path.join("received_files", "model.h5")
#         summary_path = os.path.join("received_files", "model_summary.json")

#         # Save model file
#         with open(model_path, 'wb') as f:
#             for chunk in model_file.chunks():
#                 f.write(chunk)

#         # Save summary file
#         with open(summary_path, 'w') as f:
#             f.write(summary_file.read().decode('utf-8'))

#         return JsonResponse({"status": "Model and summary received successfully"})

#     return JsonResponse({"error": "Invalid request"}, status=400)


# def request_data_from_all_clients(request):
#     clients = Client.objects.all()
#     responses = {}

#     for client in clients:
#         client_url = f"http://{client.host}:{client.port}/client/process-data/"

#         try:
#             response = requests.get(client_url)
#             responses[client.user.username] = response.json()  # Collect each client's response
#         except requests.RequestException as e:
#             responses[client.user.username] = {"error": str(e)}

#     return Response(responses)
import requests
from django.http import JsonResponse
import json
from .models import ClientInfo, ClientFile
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


@csrf_exempt
def register_client(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get("username")
        ip = data.get("ip_address")
        port = data.get("port")
        ClientInfo.objects.update_or_create(username=username, ip_address = ip, port = port)
        return JsonResponse(
            {"status": "Client registered", "ip": ip, "port": port},
            status=200
        )
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)  
    
def client_list(request):
    clients = ClientFile.objects.all()

    return render(request, 'client_list.html', {'clients': clients})

import requests
from django.http import JsonResponse
from .models import ClientInfo

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ClientFile, ClientInfo

@csrf_exempt  # Only use csrf_exempt for testing; it's recommended to use CSRF protection in production
def receive_files(request):
    if request.method == 'POST':
        if 'model' not in request.FILES or 'summary' not in request.FILES:
            return JsonResponse({"error": "Both modelFile and modelSummary are required"}, status=400)
        
        model_file = request.FILES['model']
        summary_file = request.FILES['summary']
        
        # Assume you have a client identified, e.g., `username`
        client_username = request.POST.get('username', 'default_client')
        client_info, created = ClientInfo.objects.get_or_create(username=client_username)
        
        # Save files to the model
        client_files, created = ClientFile.objects.get_or_create(username=client_info)
        client_files.modelFile.save(model_file.name, model_file)
        client_files.modellsummary.save(summary_file.name, summary_file)

        return JsonResponse({"status": "Files received successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=400)


def request_data_from_client(request):
    clients = ClientInfo.objects.all()
    results = []

    for client in clients:
        try:
            client_url = f"http://{client.ip_address}:{client.port}/client/process-data/"
            response = requests.get(client_url)

            if response.status_code == 200:
                data = response.json()
                processed_data = data.get("message", "").upper()  # Convert to uppercase
                
                # Send processed data back to client
                send_data_to_client(processed_data, client_url=client_url)
                results.append({"client": client.username, "status": "Data processed and sent"})

            else:
                results.append({"client": client.username, "status": "Failed to fetch data", "error": "Non-200 status code"})

        except requests.exceptions.RequestException as e:
            results.append({"client": client.username, "status": "Request failed", "error": str(e)})

        except ValueError as e:
            results.append({"client": client.username, "status": "Invalid JSON response", "error": str(e)})

    # Return results for all clients
    return JsonResponse({"results": results})

def send_data_to_client(data, client_url):
    try:
        response = requests.post(client_url, json={"processed_data": data})
        if response.status_code == 200:
            return {"status": "Data sent successfully"}
        else:
            return {"status": "Failed to send data", "error": "Non-200 status code"}
    except requests.exceptions.RequestException as e:
        return {"status": "Request failed", "error": str(e)}



