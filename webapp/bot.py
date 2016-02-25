#!/usr/bin/python

from motor import DCMotor
from servo import Servo
import RPi.GPIO as GPIO

import readchar
import logging

class Bot:
    'Controls bot'

    def __init__(self, logger = logging):
        self.logger = logger
        self.servo = Servo(logger = logger)
        self.dcMotor = DCMotor()
        self.moveFuncs = {
            'W': self.dcMotor.forward,
            'S': self.dcMotor.backward,
            'A': self.dcMotor.left,
            'D': self.dcMotor.right,
            'w': self.servo.up,
            's': self.servo.down,
            'a': self.dcMotor.left,
            'd': self.dcMotor.right
        }
        self.logger.info('bot created')

    def start(self):
        self.servo.start()

    def stop(self):
        self.servo.stop()

    def move(self, ch):
        self.logger.info('bot move %s' %ch)
        func = self.moveFuncs.get(ch, lambda: 'Unknown %s' %ch)
        return func()

    def setServoFine(self):
        self.servo.setFineMovement()

    def setServoCoarse(self):
        self.servo.setCoarseMovement()

    def test(self):
        'Testing bot'
        try:
            self.start()
            ch = readchar.readchar()
            while(ch != 'Q'):
                self.move(ch)
                ch = readchar.readchar()
        finally:
            self.stop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(created)f (%(threadName)-2s) %(message)s')

    try:
        bot = Bot()
        bot.test()
    finally:
        GPIO.cleanup()
