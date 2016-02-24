#!/usr/bin/python

from flask import Flask,render_template, abort
from flask import request, Response

from bot import Bot
import RPi.GPIO as GPIO


import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
bot = Bot(logger = app.logger)
bot.start()
print '***********SUMOBOT INITIATED***********'


@app.route('/robot/api/v1.0/stop', methods=['GET'])
def bot_stop():
    bot.stop()
    return Response({}, status=200, mimetype='application/json')

@app.route('/robot/api/v1.0/setFineMovement', methods=['GET'])
def setFineMovement():
    bot.setFineMovement()
    return Response({}, status=200, mimetype='application/json')

@app.route('/robot/api/v1.0/setCoarseMovement', methods=['GET'])
def setCoarseMovement():
    bot.setCoarseMovement()
    return Response({}, status=200, mimetype='application/json')

@app.route('/robot/api/v1.0/move', methods=['POST'])
def run_command():
    if not request.form or not 'ch' in request.form:
        abort(400)
    ch = request.form['ch']
    app.logger.info('Received command %s' %ch)
    bot.move(ch)
    resp = Response({}, status=200, mimetype='application/json')
    return resp

@app.route('/hangout.xml')
def hangoutXml():
    return render_template('hangout.xml')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('bot.log', maxBytes=10000000, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    try:
        bot.start()
        print '***********STARTED SUMOBOT***********'
        app.run(host='0.0.0.0', port=8080, debug=False)
    finally:
        bot.stop()
        GPIO.cleanup()
        print '***********STOPPED SUMOBOT***********'

