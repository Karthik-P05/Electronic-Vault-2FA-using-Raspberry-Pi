import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm=GPIO.PWM(12, 50)

GPIO.setup(11, GPIO.OUT)
pwm1=GPIO.PWM(11, 50)
pwm.start(0)
pwm1.start(0)



def setangle1(angle):
    duty = angle / 18 +2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    pwm.ChangeDutyCycle(0)

def setangle(angle):
    duty = angle / 18 +2
    GPIO.output(11, True)
    pwm1.ChangeDutyCycle(duty)
    sleep(1)
    pwm1.ChangeDutyCycle(0)

setangle(0)
setangle1(0)
sleep(2)
setangle(180)
setangle1(180)
#for i in range(0,181,30):
#    setangle(i)
    #time.sleep(2)
pwm.stop()
pwm1.stop()
GPIO.cleanup()
  