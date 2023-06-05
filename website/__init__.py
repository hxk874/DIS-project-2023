from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from os import path
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

#engine = create_engine('http://127.0.0.1:5000')

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
	app = Flask(__name__)

	# Configure upload file path flask
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.secret_key = 'This is your secret key to utilize session in Flask'
	app.config['SQLALCHEMY_DATABSE_URI'] = f'sqlite:///{DB_NAME}'
	
	from .views import views

	app.register_blueprint(views, url_prefix='/')

	return app


def create_database(app):
	if not path.exists('website/' + DB_NAME):
		db.create_all(app=app)
		print('Database created successfully!')








