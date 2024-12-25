from .signals import load_to_csv, training_finished, start_training, data_loaded
import os
import csv

csv_file_path = "../output.csv"
DATA_PATH = "D:/research mp 2025/Projects/client_1"

def load_imagepaths_to_csv(sender, **kwargs):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["image_path", "X", "Y", "patient_id", "classification"])
        writer.writeheader()
    folder = os.listdir(DATA_PATH)
    k = 0
    for n in range(len(folder)):
        patient_id = folder[n]
        patient_path = DATA_PATH+"/"+patient_id
        for c in [0,1]:
            class_path = patient_path+"/"+str(c)+"/"
            subfiles = os.listdir(class_path)
            for m in range(len(subfiles)):
                image_path = class_path + subfiles[m]
                coord = image_path.split("_")
                X = coord[3][:1]
                Y = coord[4][:1]
                k+1
                object = {
                    "image_path":image_path,
                    "X": X,
                    "Y":Y,
                    "patient_id":patient_id,
                    "classification":c
                }
                with open(csv_file_path, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["image_path", "X", "Y", "patient_id", "classification"])
                    writer.writerow(object)

    print("ImagePaths Loaded into csv.")
    try:
        data_loaded.send(sender=None)
        print("Dataloaded signal sent.")
    except Exception as e:
        print("inside utils, dataloaded signal not sent", e)

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