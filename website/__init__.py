from flask import *
import os
import psycopg2
import matplotlib
from distutils import debug

# application that enables plotting of data
matplotlib.use('Agg')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
IMAGE_FOLDER = os.path.join('static', 'images')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

# Connect to your database
conn = psycopg2.connect(host="localhost", user="postgres", dbname="postgres", password="password", port="5432")
cur = conn.cursor()

def create_app():
	app = Flask(__name__)

	# Configure upload file path flask
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.secret_key = 'This is your secret key to utilize session in Flask'

	from .views import views

	app.register_blueprint(views, url_prefix='/')
	return app

