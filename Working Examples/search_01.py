import hashlib
import time
from pyfingerprint.pyfingerprint import PyFingerprint
import pymysql
import cv2
import os
import face_recognition
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import pickle

# Connect to MySQL database
db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
curs = db.cursor()

# Initialize fingerprint sensor
fin = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
if not fin.verifyPassword():
    raise ValueError('The given fingerprint sensor is wrong !')

# Load facial encodings from pickle file
encodingsP = "database_enc.pickle"
print(encodingsP)
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# Initialize video stream
vs = VideoStream(0).start()
time.sleep(2.0)

while True:
    print('Waiting for finger...')
    
    # Wait for fingerprint
    while fin.readImage() == False:
        pass
        
    fin.convertImage(0x01)
    result = fin.searchTemplate()
    positionNumber = result[0]
    
    if positionNumber == -1:
        print("Fingerprint not found, ready for scan again")
        continue
    
    # Load fingerprint template
    print("Fingerprint found")
    fin.loadTemplate(positionNumber, 0x01)
    chara = str(fin.downloadCharacteristics(0x01)).encode('utf-8')
    find = hashlib.sha256(chara).hexdigest()

    # Retrieve user data from database
    query = "SELECT * FROM data11 WHERE fing_encod = %s"
    curs.execute(query, find)
    row = curs.fetchone()
    
    if not row:
        print("No user found for this fingerprint, ready for scan again")
        continue
        
    print("Fingerprint found for ID : ", row[0])
    print("Name : ", row[1])
    
    # Retrieve facial encodings for user
    result = row[4]
    data = pickle.loads(result)
    
    # Start facial recognition loop
    while True:
        # Grab frame from video stream and resize it
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        
        # Detect faces in the frame
        boxes = face_recognition.face_locations(frame)
        encodings = face_recognition.face_encodings(frame, boxes)
        
        # Loop over detected faces and check for matches with user's facial encodings
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            if True in matches:
                print("Access granted")
                #time.sleep(10)
                break
            else:
                print("Access denied")
            break
        
    
    # Release resources and close database connection
    cv2.destroyAllWindows()
    vs.stop()
    db.close()
    break
    # Start over from waiting for fingerprint
    