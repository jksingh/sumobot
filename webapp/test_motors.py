#!/usr/bin/python

from motor import DCMotor
from servo import Servo
import RPi.GPIO as GPIO
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        servo = Servo()
        servo.test()

        dcMotor = DCMotor()
        dcMotor.test()
    finally:
            GPIO.cleanup()
