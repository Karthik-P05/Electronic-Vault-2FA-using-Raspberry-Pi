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
from RPLCD.gpio import CharLCD

lcd = CharLCD(pin_rs=7, pin_e=8, pins_data = [25, 24, 23, 18],numbering_mode=GPIO.BCM, cols=16, rows=2, dotsize=8, charmap='A02', auto_linebreaks=True)
fing = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
vs = VideoStream(0).start()
time.sleep(2.0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
pwm1=GPIO.PWM(5, 50)
pwm2=GPIO.PWM(6, 50)
pwm1.start(0)
pwm2.start(0)
def servo_1(angle):
    duty = angle / 18 +2
    GPIO.output(5, True)
    pwm1.ChangeDutyCycle(duty)
    sleep(1)
    pwm1.ChangeDutyCycle(0)
    
def servo_2(angle):
    duty = angle / 18 +2
    GPIO.output(6, True)
    pwm2.ChangeDutyCycle(duty)
    sleep(1)
    pwm2.ChangeDutyCycle(0)

    #pwm.stop()
    #GPIO.cleanup()
if not fing.verifyPassword():
    raise ValueError('The given fingerprint sensor is wrong !')

while True:
    
    db = pymysql.connect(host='localhost', user='karthik', password='karthik', database='authentication')
    curs=db.cursor()
    now = datetime.datetime.now()
    
    today = now.strftime("%d-%m-%y")
    lcd.clear()
    lcd.write_string('Waiting for finger...')
    print('Waiting for finger...')
    ## Wait that finger is read
    while ( fing.readImage() == False ):
        pass
        
    fing.convertImage(0x01)
    result = fing.searchTemplate()
    positionNumber = result[0]
    if positionNumber == -1:
        lcd.clear()
        lcd.write_string('Fingerprint not found')
        print("Fingerprint not found")
        time.sleep(2)
        vs.stop()
    else:
        lcd.clear()
        lcd.write_string('Fingerprint found')
        print("Fingerprint found")
        time.sleep(2)
        fing.loadTemplate(positionNumber, 0x01)
        chara = str(fing.downloadCharacteristics(0x01)).encode('utf-8')
        find = hashlib.sha256(chara).hexdigest()

        query = "SELECT * FROM data11 WHERE fing_encod = %s"
        curs.execute(query,find)
        db.commit()
        row = curs.fetchone()
        
        iD = row[0]
        name = row[1]
        
        print("Fingerprint found for ID : ", row[0])
        print("Name : ", row[1])
        
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('ID : {}'.format(iD))
        lcd.cursor_pos = (1, 0)
        lcd.write_string('Name : {}'.format(name))
        
        time.sleep(2)
        #iD = row[0]
        #name = row[1]
        face = row[4]
        data = pickle.loads(face)
         
        with open('data_enc.pickle', 'wb') as f:
            pickle.dump(data, f)
        encodingsP = "data_enc.pickle"
        
        lcd.clear()
        lcd.write_string('loading face detector...')
        print("[INFO] loading face detector...")
        
        
        data = pickle.loads(open(encodingsP, "rb").read())
    
        time.sleep(2.0)
        
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=500)
            boxes = face_recognition.face_locations(frame)
            if len(boxes) == 0:
                
                print('No face found\n')
                lcd.clear()
                lcd.write_string('No face found')
                time.sleep(2)
                break
            encodings = face_recognition.face_encodings(frame, boxes)
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                if True in matches:
                    print("Face Matched for ID : ", iD)
                    lcd.clear()
                    lcd.write_string('Face matched for ID : {}'.format(iD))
                    time.sleep(2)
                    print("Access granted\n")
                    lcd.clear()
                    lcd.write_string('Access granted')
                    time.sleep(2)
                    sql = " INSERT INTO record1 (id, name, date, time) VALUES (%s, %s, %s, %s)"
                    curs.execute(sql, (iD,name,today,now.time()))
                    db.commit()
                    
                    #pwm.start(0)
                    #for i in range(0,181,10):
                     #   setangle(i)
                    #time.sleep(2)
                    servo_1(0)
                    servo_2(180)
                    #setangle(45)
                    #setangle(90)
                    #setangle(135)
                    servo_1(180)
                    servo_2(0)
                    
                    time.sleep(2)
                    #pwm.stop()
                    #GPIO.cleanup()
                    
                else:
                    lcd.clear()
                    lcd.write_string('Face not match')
        
                    print("Face not match")
                    time.sleep(2)
                    lcd.clear()
                    lcd.write_string('Access denied')
                    print("Access denied\n")
                    time.sleep(2)
            
            break
        servo_1(0)
        servo_2(180)
        #setangle(0)
        #pwm.stop()
        #GPIO.cleanup()
        cv2.destroyAllWindows()
        curs.close()
        db.close()
        f.close()




