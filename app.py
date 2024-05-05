from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
import logging
import datetime
import threading
import signal
import os
from db import MySQLDB
from constants import *

environ = os.environ.copy()
environ['PYTHONIOENCODING'] = 'utf-8'

app = Flask("QuanLiHS")
app.config["DEBUG"] = False

app.config["TRAP_BAD_REQUEST_ERRORS"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

if DEVELOPMENT_ENV is not None:
	#app.config["DEBUG"] = True
	APP_PORT_PRODUCTION = 8080 if os.environ.get("APP_PORT") is None else int(os.environ.get("APP_PORT"))

sio = SocketIO(app, threading=True)

# Configure the Werkzeug logger to set the logging level to WARNING
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.WARNING)
is_listening = False
log_enable = {}

@app.route("/")
def index():
	db = MySQLDB()
	all_rules = db.get_table(DATATABLE.NOIQUY.value)
	all_class = db.get_all_class()
	current_date = datetime.datetime.now()
	current_year = str(current_date.year).zfill(2)
	current_month = str(current_date.month).zfill(2)
	current_day = str(current_date.day).zfill(2)
	weeknum = current_date.isocalendar()[1]
	lastest_violate = db.get_top_x_vipham(10)
	return render_template("index.html", rules = all_rules, classes = all_class, weeknum = weeknum, current_date = f"{current_year}.{current_month}.{current_day}", lastest_data = lastest_violate)
	
@app.route("/stats", methods=["GET"])
def stats():
	db = MySQLDB()
	current_date = datetime.datetime.now()
	weeknum = request.args.get('weeknum', current_date.isocalendar()[1])
	lop = request.args.get('lop', "")
	yearlystats = db.get_yearly_stats()
	weeklystats = db.get_weekly_stats(weeknum)
	weeklydetail = db.get_weekly_detail(weeknum, lop)
	weeklyviotime = db.get_hs_vipham_trong_tuan(weeknum, lop)
	return render_template("stats.html", yearlystats = yearlystats, weeknum=weeknum, lop = lop,weeklystats = weeklystats, weeklydetail=weeklydetail, weeklyviotime = weeklyviotime)
	


@app.route('/robots.txt')
def robots():
	robots_content = "User-agent: *\nDisallow: /admin"
	return Response(robots_content, mimetype='text/plain')

def send_result_to_client(id, data, params):
	sio.emit('data', data)


@sio.on('connect')
def on_connect():
	print('Server received connection')

@sio.on('disconnect')
def on_disconnect():
	print('Client disconnected')

@sio.on('heartbeat')
def on_heartbeat(data):
	current_time = datetime.now(pytz.timezone('Asia/Bangkok'))
	sio.emit("moredata", {'req' : 'heartbeatCb', 'data' : {'ver' : SERVER_VERSION, 'time': current_time.strftime("%Y-%m-%d %H:%M:%S")} , 'ret' : 'succes'}, room = request.sid)

def run_flask():
	global app_thread
	print("Listening to port %d" % APP_PORT_PRODUCTION)
	#sio.run(app, host = '0.0.0.0', port = APP_PORT_PRODUCTION)
	app_thread = threading.Thread(target=sio.run, kwargs={"app": app, "host": "0.0.0.0", "port": APP_PORT_PRODUCTION, "log_output" : False })
	app_thread.start()

def clean(data):
	pass


def start_app():
	global app_thread
	run_flask()
	try:
		# Wait for the termination signal (Ctrl+C)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		#signal.pause()
	except KeyboardInterrupt:
		# Set the flag to stop the app and threads
		app_thread.join()


if __name__ == '__main__':
	start_app()