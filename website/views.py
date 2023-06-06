from flask import Blueprint, render_template, request, flash, jsonify
from . import app, UPLOAD_FOLDER, conn, cur
#from .models import Sample
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
#cols = ['UNIQUE_ID','TECTONIC SETTING', 'LOCATION', 'ROCK NAME','MATERIAL','ROCK TYPE', 'SIO2(WT%)', 'AL2O3(WT%)', 'CAO(WT%)', 'NA2O(WT%)', 'K2O(WT%)', 'FEO(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)', 'MGO(WT%)', 'MNO(WT%)', 'P2O5(WT%)', 'LOI(WT%)']
cols = ['UNIQUE_ID','TECTONIC SETTING', 'LOCATION', 'ROCK NAME','MATERIAL','ROCK TYPE', 'SIO2(WT%)', 'AL2O3(WT%)', 'CAO(WT%)', 'NA2O(WT%)', 'K2O(WT%)', 'FEO(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)', 'MGO(WT%)', 'MNO(WT%)', 'P2O5(WT%)', 'LOI(WT%)']

@views.route('/', methods=['GET', 'POST'])
def uploadFile():
	if request.method == 'POST':
		# upload file flask
		f = request.files.get('file')
 
 		# Extracting uploaded file name
		data_filename = secure_filename(f.filename)
		
		f.save(os.path.join(placement, data_filename))
		tablename = 'sample'
		session['uploaded_data_file_path'] = os.path.join(placement, data_filename)
		cur.execute(f"CREATE TABLE {tablename} (id SERIAL PRIMARY KEY, unique_id INT, tectonic_set VARCHAR(150), location VARCHAR(1000), rock_name VARCHAR(150), material VARCHAR(150), rock_type VARCHAR(150), siO2 FLOAT, al2o3 FLOAT, caO FLOAT, na2O FLOAT, k2O FLOAT, feO FLOAT, fe2O3 FLOAT, feO_total FLOAT, mgO FLOAT, mnO FLOAT, p2O5 FLOAT, loss FLOAT);")
		parseCSV(session['uploaded_data_file_path'],tablename)
		os.remove(os.path.join(placement, data_filename)) # remove csv file from uploads folder 

		return render_template('index2.html')
	return render_template("index.html")


def parseCSV(filePath, tablename):
	# CVS Column Names
	
	# Use Pandas to parse the CSV file
	csvData = pd.read_csv(filePath, usecols=cols, encoding='unicode_escape')
	csvData.dropna(subset='UNIQUE_ID',axis=0, inplace=True)
    # Loop through the Rows
	
	for index, row in csvData.iterrows():
		sql = "INSERT INTO sample (unique_id, tectonic_set, location, rock_name, material, rock_type, siO2, al2o3, caO, na2O, k2O, feO, fe2O3, feO_total, mgO, mnO, p2O5, loss) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (
				#tablename,
				row['UNIQUE_ID'], 
				row['TECTONIC SETTING'], 
				row['LOCATION'],
				row['ROCK NAME'], 
				row['MATERIAL'], 
				row['ROCK TYPE'], 
				row['SIO2(WT%)'],
				row['AL2O3(WT%)'], 
				row['CAO(WT%)'],
				row['NA2O(WT%)'],
				row['K2O(WT%)'],
				row['FEO(WT%)'],
				row['FE2O3(WT%)'],
				row['FEOT(WT%)'],
				row['MGO(WT%)'],
				row['MNO(WT%)'],
				row['P2O5(WT%)'],
				row['LOI(WT%)']
				)
		cur.execute(sql, values)
		conn.commit()
	return render_template("index.html")


           




"""@views.route('/', methods=['GET', 'POST'])
def uploadFile():
	if request.method == 'POST':
	    # upload file flask
		f = request.files.get('file')

		# Extracting uploaded file name
		data_filename = secure_filename(f.filename)

		f.save(os.path.join(placement, data_filename))

		session['uploaded_data_file_path'] = os.path.join(placement, data_filename)

		#data_file_path = session.get('uploaded_data_file_path', None)

		#data = pd.read_csv(data_file_path, usecols=cols, encoding='unicode_escape')
        #data.dropna(subset='UNIQUE_ID',axis=0, inplace=True)
        #os.remove(os.path.join(placement, data_filename))
        # use columns location hovedelementer rocktype tectonic setting. add column Project number, user ID
        # add as Sample model to database 
        # delete file from uploads (os.remove(os.path.join(placement, data_filename)) )
        return render_template('index2.html')
	return render_template("index.html")"""


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