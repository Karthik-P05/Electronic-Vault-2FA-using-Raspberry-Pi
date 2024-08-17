import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12,GPIO.OUT)

servo = GPIO.PWM(12,50)

servo.start(0)

try:
    while True:
        angle = float(input("Enter a angle : "))
        servo.ChangeDutyCycle(2+(angle/18))
        time.sleep(0.5)
        
finally:
    servo.stop()
    GPIO.cleanup()