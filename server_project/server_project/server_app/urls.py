# server_project/urls.py
from django.contrib import admin
from django.urls import path
from server_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('request-data/', views.request_data_from_client, name='request-data'),
    path('register-client/', views.register_client, name = 'register-client'),          
    path('clients/', views.client_list, name='client-list'),
    path('server/receive-files/', views.receive_files, name='receive_files'),


]

