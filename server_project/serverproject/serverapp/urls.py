from django.urls import path
from .views import RegisterClientView, DeregisterClientView, StartTrainingView

urlpatterns = [
    path("register/", RegisterClientView.as_view(), name= "register"),
    # path("deregister/", DeregisterClientView.as_view(), name= "deregister"),
    path("start_training/", StartTrainingView.as_view(), name="start_training")
]
