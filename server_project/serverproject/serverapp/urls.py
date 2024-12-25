from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterClientView.as_view(), name= "register"),
    # path("deregister/", DeregisterClientView.as_view(), name= "deregister"),
    path("start_training/", views.startRound, name="start_training"),
    path("recieve-files/", views.RecieveFiles, name="receive_models"),
]
