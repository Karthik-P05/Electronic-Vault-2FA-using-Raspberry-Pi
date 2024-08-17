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
import datetime
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

fing = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
vs = VideoStream(0).start()
time.sleep(2.0)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm=GPIO.PWM(12, 50)
pwm.start(0)
def setangle(angle):
    duty = angle / 18 +2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    pwm.ChangeDutyCycle(0)
    #pwm.stop()
    #GPIO.cleanup()
if not fing.verifyPassword():
    raise ValueError('The given fingerprint sensor is wrong !')

while True:
    
    db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
    curs=db.cursor()
    now = datetime.datetime.now()
    
    today = now.strftime("%d-%m-%y")
    print('Waiting for finger...')
    ## Wait that finger is read
    while ( fing.readImage() == False ):
        pass
        
    fing.convertImage(0x01)
    result = fing.searchTemplate()
    positionNumber = result[0]
    if positionNumber == -1:
        print("Fingerprint not found")
        vs.stop()
    else:
        
        print("Fingerprint found")
        fing.loadTemplate(positionNumber, 0x01)
        chara = str(fing.downloadCharacteristics(0x01)).encode('utf-8')
        find = hashlib.sha256(chara).hexdigest()

        query = "SELECT * FROM data11 WHERE fing_encod = %s"
        curs.execute(query,find)
        db.commit()
        row = curs.fetchone()
        print("Fingerprint found for ID : ", row[0])
        print("Name : ", row[1])
        iD = row[0]
        name = row[1]
        face = row[4]
        data = pickle.loads(face)
         
        with open('data_enc.pickle', 'wb') as f:
            pickle.dump(data, f)
        encodingsP = "data_enc.pickle"
    
        print("[INFO] loading face detector...")
        data = pickle.loads(open(encodingsP, "rb").read())
    
        time.sleep(2.0)
        
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=500)
            boxes = face_recognition.face_locations(frame)
            if len(boxes) == 0:
                print('No face found\n')
                break
            encodings = face_recognition.face_encodings(frame, boxes)
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                if True in matches:
                    print("Face Matched for ID : ", iD)
                    print("Access granted\n")
                    sql = " INSERT INTO record1 (id, name, date, time) VALUES (%s, %s, %s, %s)"
                    curs.execute(sql, (iD,name,today,now.time()))
                    db.commit()
                    
                    pwm.start(0)
                    #for i in range(0,181,10):
                     #   setangle(i)
                    #time.sleep(2)
                    setangle(0)
                    #setangle(45)
                    #setangle(90)
                    #setangle(135)
                    setangle(180)
                    
                    time.sleep(2)
                    #pwm.stop()
                    #GPIO.cleanup()
                    
                else:
                    print("Face not match")
                    print("Access denied\n")
            
            break
        setangle(0)
        #pwm.stop()
        #GPIO.cleanup()
        cv2.destroyAllWindows()
        curs.close()
        db.close()
        f.close()


