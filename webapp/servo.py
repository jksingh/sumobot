import RPi.GPIO as GPIO
import sched, time
import logging
import threading

class Servo:
    'Controls servo motor'

    def __init__(self, logger = logging):

        # constants
        self.pin = 40
        self.startPosition = 4
        self.endPosition = 8
        self.frontPosition = 5
        self.step = 0.25
        self.wait = 0.5
        self.sleepAfter = 30

        self.position = self.frontPosition

        self.logger = logger

        self.operationCount = 0
        self.stopped = True
        self.rlock = threading.RLock()

        self.schedulerThread = threading.Thread(name='AutoStop', target = self.__autoStop, args = ())
        self.schedulerThread.setDaemon(True)
        self.schedulerThread.start()
        self.logger.info('servo initiated')

    def __autoStop(self):
        try:
            time.sleep(self.sleepAfter)
            self.logger.info('servo autostop')
            self.stop()
        except:
            pass
        self.__autoStop()

    def start(self):
        'Call before any motion'
        with self.rlock:
            if(self.stopped):
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.pin, GPIO.OUT)
                self.pwm=GPIO.PWM(self.pin, 50)
                self.pwm.start(self.position)
                self.stopped = False
                self.logger.info('servo started')

    def stop(self):
        'Call after if motion is no longer required'
        with self.rlock:
            if(self.stopped == False):
                self.pwm.stop()
                self.stopped = True
                self.logger.info('servo stopped')

    def setFineMovement(self):
        self.step = 0.25
        self.logger.info('servo set to fine movement')

    def setCoarseMovement(self):
        self.step = 0.5
        self.logger.info('servo set to coarse movement')

    def up(self):
        if(self.position <= self.endPosition):
            self.start()
            self.position = self.position + self.step
            self.pwm.ChangeDutyCycle(self.position)
            time.sleep(self.wait)
            self.logger.info('servo up = %f', self.position)

    def down(self):
        if(self.position >= self.startPosition):
            self.start()
            self.position = self.position - self.step
            self.pwm.ChangeDutyCycle(self.position)
            time.sleep(self.wait)
            self.logger.info('servo down = %f' % self.position)

    def test(self):
        'Testing servo'
        try:
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
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(created)f (%(threadName)-2s) %(message)s')

    try:
        servo = Servo()
        servo.test()
    finally:
        GPIO.cleanup()

