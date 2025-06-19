import hashlib
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from RPi import GPIO
import pymysql
import cv2
import os
from imutils import paths
import face_recognition
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle

db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
curs=db.cursor()

fing = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

if not fing.verifyPassword():
    raise ValueError('The given fingerprint sensor is wrong !')

def start():
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( fing.readImage() == False ):
        pass
        
    fing.convertImage(0x01)
    result = fing.searchTemplate()
    positionNumber = result[0]
    #fin = f.downloadCharacteristics()
    

    if positionNumber == -1:
        print("Fingerprint not found")
    else:
        print("Fingerprint found")
        fing.loadTemplate(positionNumber, 0x01)
        chara = str(fing.downloadCharacteristics(0x01)).encode('utf-8')
        find = hashlib.sha256(chara).hexdigest()
        query = "SELECT * FROM data11 WHERE fing_encod = %s"
        curs.execute(query,find)
    
        row = curs.fetchone()
        print("Fingerprint found for ID : ", row[0])
        print("Name : ", row[1])
        
        face = row[4]
    
        data = pickle.loads(face)
        
        #Determine faces from encodings.pickle file model created from train_model.py
        encodingsP = "data_enc.pickle"
        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
        print("[INFO] loading encodings + face detector...")
        data = pickle.loads(open(encodingsP, "rb").read())
        # initialize the video stream and allow the camera sensor to warm up
        vs = VideoStream(0).start()
        with open('data_enc.pickle', 'wb') as f:
            pickle.dump(data, f)
        time.sleep(2.0)
        while True:
            # grab the frame from the threaded video stream and resize it
            # to 500px (to speedup processing)
            frame = vs.read()
            frame = imutils.resize(frame, width=500)
            # Detect the fce boxes
            boxes = face_recognition.face_locations(frame)
            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(frame, boxes)
            # loop over the facial embeddings
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"],
                    encoding)
                if True in matches:
                    print("Access granted")
                    #vs.release()
                else:
                    print("Access denied")
            break
        cv2.imshow("Facial Recognition is Running", frame)
            
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        f.close()

        
while True:
    
    print("----------------")
    print("PRESS 'S' START")
    print("----------------")
    c = input("> ")

    if c == "s":
        start()
        

        