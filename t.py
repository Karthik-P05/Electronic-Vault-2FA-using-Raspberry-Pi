import os
import cv2
import numpy as np

# Define the path to the dataset
dataset_path = "dataset"

# Initialize the face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Create a list of faces and labels from the dataset
faces = []
labels = []
folders = os.listdir(dataset_path)
for i, folder_name in enumerate(folders):
    folder_path = os.path.join(dataset_path, folder_name)
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        faces.append(image)
        labels.append(i)

# Train the face recognizer
recognizer.train(faces, np.array(labels))

# Save the trained model to a file
recognizer.save("trainer.yml")