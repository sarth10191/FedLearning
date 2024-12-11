from django.dispatch import receiver
from signals import start_training

def load_data(sender, **kwargs):
    print("started loading data")
    
start_training.connect(load_data)