#! /usr/bin/python

# import the necessary packages
from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2
import os
import pymysql


db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
curs=db.cursor()


# provide folder name as input
name = input("Name : ")

#construct the path to the folder containing the images
folder_path = os.path.join("dataset",name)
# our images are located in the dataset folder
print("[INFO] start processing faces...")
imagePaths = list(paths.list_images(folder_path))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model="hog")

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()

with open('encodings.pickle', 'rb') as h:
    data = pickle.load(h)
data_bin = pickle.dumps(data)

curs.execute('INSERT INTO images (name,img_data) VALUES (%s, %s)',(name,data_bin))
db.commit()
db.close()
