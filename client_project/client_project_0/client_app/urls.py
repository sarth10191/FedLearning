from django.urls import path
from . import views


from django.urls import path
from . import views

urlpatterns = [
    path('process-data/', views.process_data, name='process-data'),
    path('receive-data/', views.receive_data, name='receive-data'),
    # path('register/', views.register_with_server, name='register'),
    # path('train-and-send/', views.train_and_send_model, name='train-and-send'),
]