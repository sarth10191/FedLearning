import django.dispatch
start_training = django.dispatch.Signal()

load_to_csv = django.dispatch.Signal()
data_loaded = django.dispatch.Signal()
start_training = django.dispatch.Signal()
training_finished = django.dispatch.Signal()