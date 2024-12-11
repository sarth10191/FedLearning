from django.urls import path
from .views import StartTrainingView
urlpatterns = [
    path("start_training/", StartTrainingView.as_view(), name="start_training")
]
