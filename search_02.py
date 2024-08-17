import hashlib
import time
from pyfingerprint.pyfingerprint import PyFingerprint
#from RPLCD.gpio import CharLCD
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

fin = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

if not fin.verifyPassword():
    raise ValueError('The given fingerprint sensor is wrong !')

while True:
    while True:
        
        print('Waiting for finger...')
        

    # Wait that finger is read
        while ( fin.readImage() == False ):
            pass
        
        fin.convertImage(0x01)
        result = fin.searchTemplate()
        positionNumber = result[0]
    #fin = f.downloadCharacteristics()
    
        if positionNumber == -1:
            print("Fingerprint not found")
        
        else:
        
    #template = f.downloadCharacteristics()
            print("Fingerprint found")
            fin.loadTemplate(positionNumber, 0x01)
            chara = str(fin.downloadCharacteristics(0x01)).encode('utf-8')
            find = hashlib.sha256(chara).hexdigest()

            query = "SELECT * FROM data11 WHERE fing_encod = %s"
            curs.execute(query,find)
    
            row = curs.fetchone()
            fing = row[4]

        #id = float(row[0])
            print("Fingerprint found for ID : ", row[0])
            print("Name : ", row[1])
            
        break
    data = pickle.loads(fing)


    with open('database_enc.pickle', 'wb') as f:
        pickle.dump(data, f)
#Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "database_enc.pickle"
    print(encodingsP)
# load the known faces and embeddings along with OpenCV's Haarcascade for face detection
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())

# initialize the video stream and allow the camera sensor to warm up
    vs = VideoStream(0).start()
    time.sleep(2.0)


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
	#names = []

	# loop over the facial embeddings
        for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
            matches = face_recognition.compare_faces(data["encodings"],
				encoding)
		# check to see if we have found a match
            if True in matches:
                print("Access granted\n\n")
                cv2.destroyAllWindows()
                vs.stop()
                f.close()
                #time.sleep(10)

            else:
                print("Access denied\n\n")
                cv2.destroyAllWindows()
                vs.stop()
                f.close()
            
        


	# display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)
    #key = cv2.waitKey(1) & 0xFF
        
	
# do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        f.close()
        break
     