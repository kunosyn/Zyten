from flask import Flask
from threading import Thread;
import logging;
import random;
import os;

app = Flask('')
log = logging.getLogger('werkzeug');
log.disabled = True;

@app.route('/')

def home():
	return "Server is up.";

def run():
  app.run(
		host="0.0.0.0",
		port=random.randint(2000,9000)
	);

def ping_server():
  '''
  Creates and starts new thread that runs the function run.
  '''
  t = Thread(target=run);
  t.start();
  