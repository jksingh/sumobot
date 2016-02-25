#!/usr/bin/python

from flask import Flask,render_template, abort
from flask import request, Response
from werkzeug.serving import run_simple
import ssl

from bot import Bot
import RPi.GPIO as GPIO


import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

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
    formatter = logging.Formatter("[%(asctime)s] [%(threadName)s:%(name)s] {%(module)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('log/bot.log', maxBytes=10000000, backupCount=5)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    log = logging.getLogger('werkzeug')
    log.addHandler(handler)
    log.setLevel(logging.INFO)

    try:
        bot = Bot(logger = app.logger)
        bot.start()
        app.logger.info('***********STARTED SUMOBOT***********')
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain('server.crt', 'server.key')
        run_simple('0.0.0.0', 8443, app, ssl_context=context)
        #context.use_privatekey_file('/home/pi/sumobot/webapp/server.key')
        #context.use_certificate_file('/home/pi/sumobot/webapp/server.crt')
        #app.run(use_reloader=True, host='0.0.0.0',port=8080,ssl_context = context, debug=False)
        #context = ('server.crt', 'server.key')
        #app.run(host='0.0.0.0', port=8080, debug=False, ssl_context=context)
    finally:
        bot.stop()
        GPIO.cleanup()
        app.logger.info('***********STOPPED SUMOBOT***********')

