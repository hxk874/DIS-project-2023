from flask import Blueprint, render_template, request, flash, jsonify
from . import db, app, UPLOAD_FOLDER
import json
from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from os import path
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

views = Blueprint('views', __name__)


placement = 'website/'+str(UPLOAD_FOLDER)
cols = ['UNIQUE_ID','TECTONIC SETTING', 'LOCATION', 'ROCK NAME','MATERIAL','ROCK TYPE', 'SIO2(WT%)', 'AL2O3(WT%)', 'CAO(WT%)', 'NA2O(WT%)', 'K2O(WT%)', 'FEO(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)', 'MGO(WT%)', 'MNO(WT%)', 'P2O5(WT%)', 'LOI(WT%)']

@views.route('/', methods=['GET', 'POST'])
def uploadFile():
	if request.method == 'POST':
	    # upload file flask
		f = request.files.get('file')

		# Extracting uploaded file name
		data_filename = secure_filename(f.filename)

		f.save(os.path.join(placement, data_filename))

		session['uploaded_data_file_path'] = os.path.join(placement, data_filename)

		data_file_path = session.get('uploaded_data_file_path', None)

		data = pd.read_csv(data_file_path, usecols=cols, encoding='unicode_escape')
        #data.dropna(subset='UNIQUE_ID',axis=0, inplace=True)
        #os.remove(os.path.join(placement, data_filename))
        # use columns location hovedelementer rocktype tectonic setting. add column Project number, user ID
        # add as Sample model to database 
        # delete file from uploads (os.remove(os.path.join(placement, data_filename)) )
        #return render_template('index2.html')
	return render_template("index.html")


@views.route('/show_data')
def showData():
	# Uploaded File Path
	data_file_path = session.get('uploaded_data_file_path', None)
	# read csv
	uploaded_df = pd.read_csv(data_file_path, encoding='unicode_escape')
	
	# hent fil ..

	# Converting to html Table
	uploaded_df_html = uploaded_df.to_html()
	return render_template('show_data.html', data_var=uploaded_df_html)