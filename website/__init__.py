from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from os import path
from werkzeug.utils import secure_filename
import psycopg2

UPLOAD_FOLDER = os.path.join('static', 'uploads')
IMAGE_FOLDER = os.path.join('static', 'images')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

conn = psycopg2.connect(host="localhost", user="postgres", dbname="dis2023", password="wildeisfine",port="5432")
cur = conn.cursor()

def create_app():
	app = Flask(__name__)

	# Configure upload file path flask
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.secret_key = 'This is your secret key to utilize session in Flask'
	
	#db.init_app(app)

	from .views import views
	#from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	return app

