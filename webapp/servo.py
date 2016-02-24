import RPi.GPIO as GPIO
import time
import logging

class Servo:
    'Controls servo motor'

    def __init__(self):

        # constants
        self.pin = 40
        self.startPosition = 4
        self.endPosition = 8
        self.frontPosition = 5
        self.step = 0.5
        self.wait = 0.5

        self.position = self.frontPosition

    def start(self):
        'Call before any motion'
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm=GPIO.PWM(self.pin, 50)
        self.pwm.start(self.position)
        logging.debug('servo started')

    def setFineMovement(self):
        self.step = 0.25

    def setCoarseMovement(self):
        self.step = 0.5
        
    def up(self):
        if(self.position <= self.endPosition):
            self.position = self.position + self.step
            self.pwm.ChangeDutyCycle(self.position)
            time.sleep(self.wait)
        logging.debug('servo up = %d' % self.position)

    def down(self):
        if(self.position >= self.startPosition):
            self.position = self.position - self.step
            self.pwm.ChangeDutyCycle(self.position)
            time.sleep(self.wait)
        logging.debug('servo down = %d' % self.position)

    def stop(self):
        'Call after if motion is no longer required'
        self.pwm.stop()
        logging.debug('servo stopped')

    def test(self):
        'Testing servo'
        try:
            self.start()
            while(self.position <= self.endPosition):
                self.up()
            while(self.position >= self.startPosition):
                self.down()
            while(self.position <= self.endPosition):
                self.up()
            while(self.position >= self.frontPosition):
                self.down()
        finally:
            self.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        servo = Servo()
        servo.test()
    finally:
        GPIO.cleanup()

