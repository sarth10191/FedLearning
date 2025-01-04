from .signals import load_to_csv, training_finished, start_training, data_loaded
import os
import csv
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import load_img, img_to_array

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


def load_images_from_csv(csv_file_path = csv_file_path):
    images = []
    df = pd.read_csv(csv_file_path)
    for path in df["image_path"]:
        image = load_img(path, target_size = (50,50))
        image_array = img_to_array(image)/255.0
        images.append(image)
    images = np.array(images)
    labels = df["classification"]
    return images, labels
#https://chatgpt.com/share/67790c6a-f924-8001-a97f-c2951891533a
#SAVE DATA IN LOADED FORMAT ON DISK TO SAVE SPACE.
#LOAD AND RESAVE WHEN ADDING MORE DATA.


def train_and_save_model(sender, path,  **kwargs):
    """
    Read class, imagepaths from the CSV file and load images from paths. 
    Train model and save it into h5 file. 
    Send a signal to let server know knowledge training is done.
    """
    model = models.load_model(path)
    data, labels = load_images_from_csv()
    data = tf.data.Dataset.from_tensor_slices((data, labels))
    model.fit(data, epochs = 1)
    model.save(path)
    training_finished.send(sender=None)

start_training.connect(train_and_save_model)