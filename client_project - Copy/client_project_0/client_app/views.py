from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import socket
import requests
# from .train_model import train_and_save_model
# import os


# def train_and_send_model(request):
#     train_and_save_model()

#     model_file_path = "model.h5"
#     summary_file_path = "model_summary.json"
#     server_url = "http://127.0.0.1:8000/server/receive-model/"

#     train_and_send_model()
#     with open(model_file_path, "rb") as model_file, open(summary_file_path, "rb") as summary_file:
#         response = requests.post(
#             server_url,
#             files={
#                 'model':model_file,
#                 'summary':summary_file
#             },
#         )

#     model_file.close()
#     summary_file.close()

#     os.remove(model_file_path)
#     os.remove(summary_file_path)

#     return JsonResponse(response)


def register_with_server():
    server_url = "http://127.0.0.1:8000/server/register-client/"
    # hostname = socket.gethostname()
    # client_ip = socket.gethostbyname(hostname)
    client_ip = "127.0.0.1" #change in production
    port = 8002
    try:
        response = requests.post(server_url, json={
            "username":"client_1",
            "ip_address":client_ip,
            "port":port,
        })
        if response.status_code == 200:
            print("Client registered Successfully.")
        else:
            print(f"Failed to register to server.{response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error registering to server: {e}")


def process_data(request):
    # Simulate data processing on the client-side
    data = {"message": "hello from client"}
    return JsonResponse(data)

@csrf_exempt
def receive_data(request):
    if request.method == "POST":
        received_data = request.body.decode('utf-8')  # Ensure correct decoding
        print(f"Received processed data from server: {received_data}")
    return JsonResponse({"status": "Data received by client"})