import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
servoPin=3
GPIO.setup(servoPin, GPIO.OUT)
pwm=GPIO.PWM(servoPin, 50)
pwm.start(servoState)
pos=5
# dont change limit
while(pos > 3 and pos < 9):
    pwm.ChangeDutyCycle(pos)
    pos = input("new pos: ")

pwm.stop()
GPIO.cleanup()


