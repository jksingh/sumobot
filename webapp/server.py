#!/usr/bin/python

from flask import Flask,render_template
from bot import Bot
from flask import request

import logging

app = Flask(__name__)

bot = Bot()
bot.start()

@app.route('/robot/api/v1.0/stop', methods=['GET'])
def bot_stop():
	bot.stop()

@app.route('/robot/api/v1.0/move', methods=['POST'])
def run_command():
	if not request.json or not 'ch' in request.json:
		abort(400)
	ch = request.json['ch']
	logging.debug('Received command %s' %ch)
	bot.move(ch)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	app.run(port=8080, debug=True)
