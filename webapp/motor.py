import RPi.GPIO as GPIO
import time
import logging

class DCMotor:
    'Controls dc motor motor'

    def __init__(self):

        # constants
        self.rightAPin = 11
        self.rightBPin = 12
        self.leftAPin = 15
        self.leftBPin = 16
        self.wait = 0.5

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.rightAPin, GPIO.OUT)
        GPIO.setup(self.rightBPin, GPIO.OUT)
        GPIO.setup(self.leftAPin, GPIO.OUT)
        GPIO.setup(self.leftBPin, GPIO.OUT)
        logging.debug('dc motor started')

    def forward(self):
        self.__rightForward()
        self.__leftForward()
        time.sleep(self.wait)
        self.__stop()
        logging.debug('dc motor forward')

    def backward(self):
        self.__rightBackward()
        self.__leftBackward()
        time.sleep(self.wait)
        self.__stop()
        logging.debug('dc motor backward')

    def right(self):
        self.__rightForward()
        self.__leftBackward()
        time.sleep(self.wait)
        self.__stop()
        logging.debug('dc motor right')

    def left(self):
        self.__rightBackward()
        self.__leftForward()
        time.sleep(self.wait)
        self.__stop()
        logging.debug('dc motor left')

    def test(self):
        'Testing dc motor'
        self.forward()
        time.sleep(self.wait)
        self.backward()
        time.sleep(self.wait)
        self.right()
        time.sleep(self.wait)
        self.left()

    def __rightForward(self):
        GPIO.output(self.rightAPin,GPIO.LOW)
        GPIO.output(self.rightBPin,GPIO.HIGH)

    def __rightBackward(self):
        GPIO.output(self.rightAPin,GPIO.HIGH)
        GPIO.output(self.rightBPin,GPIO.LOW)

    def __leftForward(self):
        GPIO.output(self.leftAPin,GPIO.LOW)
        GPIO.output(self.leftBPin,GPIO.HIGH)

    def __leftBackward(self):
        GPIO.output(self.leftAPin,GPIO.HIGH)
        GPIO.output(self.leftBPin,GPIO.LOW)

    def __stop(self):
        GPIO.output(self.rightAPin,GPIO.LOW)
        GPIO.output(self.rightBPin,GPIO.LOW)

        GPIO.output(self.leftAPin,GPIO.LOW)
        GPIO.output(self.leftBPin,GPIO.LOW)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        dcMotor = DCMotor()
        dcMotor.test()
    finally:
        GPIO.cleanup()


