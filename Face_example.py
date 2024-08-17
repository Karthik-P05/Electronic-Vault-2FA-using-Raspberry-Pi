import pymysql
import cv2, os, sys, time
import numpy as np
from PIL import Image
import face_recognition
import os
from imutils import paths
import pickle
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import time
import shutil

#db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
#curs=db.cursor()

def enroll():
    downloads_path = os.path.expanduser('~/facial rec/dataset')

    folder_name = input('Name : ') #replace with your name
    folder_path = os.path.join(downloads_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'Created folder: {folder_path}')
    else:
        print(f'Folder already exists: {folder_path}')
    
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("press space to take a photo", 500, 300)

    count = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("press space to take a photo", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
        
            file_path = os.path.join(folder_path, f'img' +str(count)+'.jpg')
            #img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
            cv2.imwrite(file_path, frame)
            print("{} written!".format(file_path))
            count += 1

    cam.release()

    cv2.destroyAllWindows()

def search():
    
    print("[INFO] start processing faces...")
    imagePaths = list(paths.list_images("dataset"))

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
    
    
    #Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
    #Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())

# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
#vs = VideoStream(src=2,framerate=10).start()
    vs = VideoStream(0).start()
    time.sleep(2.0)

# start the FPS counter
    fps = FPS().start()

# loop over frames from the video file stream
    while True:
	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
	# Detect the fce boxes
        boxes = face_recognition.face_locations(frame)
	# compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []

	# loop over the facial embeddings
        for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
            matches = face_recognition.compare_faces(data["encodings"],
			encoding)
            name = "Unknown" #if face is not recognized, then print Unknown

		# check to see if we have found a match
            if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                #If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    print(currentname)

		# update the list of names
            names.append(name)

	# loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
		# draw the predicted face name on the image - color is in BGR
            cv2.rectangle(frame, (left, top), (right, bottom),
                    (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                .8, (0, 255, 255), 2)

	# display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF

	# quit when 'q' key is pressed
        if key == ord("q"):
            break

	# update the FPS counter
        fps.update()

# stop the timer and display FPS information
    fps.stop()
    #print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    
def delete():
        
    downloads_path = os.path.expanduser('~/facial rec/dataset')

    folder_name = input('Name of User to be deleted :') #replace with your name
    folder_path = os.path.join(downloads_path, folder_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f'Deleted face id of {folder_name}')
    else:
        print(f'{folder_name} not exists')
    



while True:
    
    print("----------------")
    print("Choose an option")
    print("e) enroll face")
    print("f) find face")
    print("d) delete face")
    print("----------------")
    c = input("> ")

    if c == "e":
        enroll()
        
    if c == "f":
        search()
        
    if c == "d":
        delete()

