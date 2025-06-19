import hashlib
import time
from pyfingerprint.pyfingerprint import PyFingerprint
#from RPi import GPIO
import RPi.GPIO as GPIO
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
GPIO.setwarnings(False)

#from gpiozero import AngularServo
#from time import sleep

#servo = AngularServo(18, min_pulse_width=0.0006,max_pulse_width=0.0023)

#GPIO.setmode(GPIO.BOARD)
#s_pin = 12
#GPIO.setup(12,GPIO.OUT)

#servo = GPIO.PWM(12, 50)

#servo.start(0)

def rotate_servo(angle):
    dc = 2 + (angle/18)
    #GPIO.output(12, True)
    servo.ChangeDutyCycle(dc)
    time.sleep(1)
    servo.ChangeDutyCycle(0)
    #servo.stop()
    #GPIO.cleanup()

#fing = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
vs = VideoStream(0).start()
time.sleep(2.0)
#if not fing.verifyPassword():
 #   raise ValueError('The given fingerprint sensor is wrong !')

while True:
    fing = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
#vs = VideoStream(0).start()
#time.sleep(2.0)
    if not fing.verifyPassword():
        raise ValueError('The given fingerprint sensor is wrong !')
    db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
    curs=db.cursor()
    now = datetime.datetime.now()
    
    GPIO.setmode(GPIO.BOARD)
    s_pin = 12
    GPIO.setup(s_pin,GPIO.OUT)

    servo = GPIO.PWM(s_pin,50)
    servo.start(0)
    #set_angle(0)
    #time.sleep(1)
    #servo.min()
    
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
                   print('No face found')
                   break
            encodings = face_recognition.face_encodings(frame, boxes)
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                if True in matches:
                    print("Face Matched for ID : ", iD)
                    print("Access granted\n")
                    #servo.start(0)
                    #servo.ChangeDutyCycle(7)
                    #time.sleep(1)
                    #servo.ChangeDutyCycle(8)
                    #time.sleep(1)
                    #servo.ChangeDutyCycle(9)
                    #time.sleep(1)
                    #servo.ChangeDutyCycle(10)
                    #time.sleep(1)
                    #servo.ChangeDutyCycle(12)
                    rotate_servo(180)
                    time.sleep(1)
                    rotate_servo(0)
                    #servo.start(100)
                    time.sleep(1)
                    rotate_servo(180)
                    #servo.stop()
                    #GPIO.cleanup()
                    #servo.ChangeDutyCycle(0)
                    #time.sleep(1)
                    #servo.angle = 90
                    #sleep(2)
                    #servo.angle = 0
                    #sleep(2)
                    #servo.angle = -90
                    #sleep(2)
                    servo.stop()
                    GPIO.cleanup()
                    sql = " INSERT INTO record1 (id, name, date, time) VALUES (%s, %s, %s, %s)"
                    curs.execute(sql, (iD,name,today,now.time()))
                    db.commit()
                    
                    
                    
                else:
                    print("Face not match")
                    print("Access denied\n")
            break
        #servo.stop()
        #GPIO.cleanup()
        #servo.start(0)
        #GPIO.cleanup()
        #cv2.destroyAllWindows()
        #rotate_servo(0)
        curs.close()
        db.close()
        f.close()
        

