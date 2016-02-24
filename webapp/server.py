#!/usr/bin/python

from flask import Flask,render_template, abort
from bot import Bot
from flask import request, Response

import logging

app = Flask(__name__)

bot = Bot()
bot.start()

@app.route('/robot/api/v1.0/stop', methods=['GET'])
def bot_stop():
	bot.stop()

@app.route('/robot/api/v1.0/move', methods=['POST'])
def run_command():
	if not request.form or not 'ch' in request.form:
		abort(400)
	ch = request.form['ch']
	logging.debug('Received command %s' %ch)
	bot.move(ch)
        resp = Response({}, status=200, mimetype='application/json')
        return resp

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
