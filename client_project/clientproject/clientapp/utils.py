from .signals import *

def load_imagepaths_to_csv(sender, **kwargs):
    print("ImagePaths Loaded into csv.")
    data_loaded.send(sender=sender)

load_to_csv.connect(load_imagepaths_to_csv)

def train_and_save_model(sender, **kwargs):
    """
    Read class, imagepaths from the CSV file and load images from paths. 
    Train model and save it into h5 file. 
    Send a signal to let server know knowledge training is done.
    """
    print("Inside function train_and_save_model. Training is finished.")
    training_finished.send(sender=None)

start_training.connect(train_and_save_model)