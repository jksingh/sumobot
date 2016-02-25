#!/usr/bin/python

from motor import DCMotor
from servo import Servo
import RPi.GPIO as GPIO
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(created)f (%(threadName)-2s) %(message)s')

    try:
        servo = Servo()
        dcMotor = DCMotor()

        servo.test()
        dcMotor.test()

        servo.setFineMovement()
        dcMotor.setFineMovement()

        servo.test()
        dcMotor.test()

    finally:
            GPIO.cleanup()
