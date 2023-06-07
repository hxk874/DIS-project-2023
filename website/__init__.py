from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from os import path
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy # ILLEGAL
import psycopg2

#engine = create_engine('http://127.0.0.1:5000')

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

#db = SQLAlchemy()
#DB_NAME = "database.db"

# database url: jdbc:postgresql://localhost:5432/postgres

conn = psycopg2.connect(host="localhost", user="postgres", dbname="postgres", password="nh3M9",port="5432")
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

