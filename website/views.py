from flask import Blueprint, render_template, request, flash, jsonify, url_for
from . import app, UPLOAD_FOLDER, conn, cur, IMAGE_FOLDER
from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from os import path
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


views = Blueprint('views', __name__)


placement = 'website/'+str(UPLOAD_FOLDER)
cols = ['UNIQUE_ID','TECTONIC SETTING', 'LOCATION', 'ROCK NAME','MATERIAL','ROCK TYPE', 'SIO2(WT%)', 'AL2O3(WT%)', 'CAO(WT%)', 'NA2O(WT%)', 'K2O(WT%)', 'FEO(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)', 'MGO(WT%)', 'MNO(WT%)', 'P2O5(WT%)', 'LOI(WT%)']

@views.route("/", methods=['GET'])
def info():
	return render_template("info.html")


@views.route('/upload', methods=['GET', 'POST'])
def uploadFile():
	if request.method == 'POST':
		
		
		tablename = str(request.form.get('tableName'))
		tablename = tablename.replace(' ', '_')
		try: # check if table already exists
			check = "SELECT * FROM ;"
			cur.execute(check[:14]+tablename+check[14:])
			conn.commit()
			if cur.fetchone():
				flash('tablename already exists!', category='error')
		except: 
			cur.execute("ROLLBACK")
			conn.commit()
			tablename = request.form.get('tableName')
			tablename = tablename.replace(' ', '_')
			# upload file flask
			f = request.files.get('file')
			# Extracting uploaded file name
			data_filename = secure_filename(f.filename)
			
			f.save(os.path.join(placement, data_filename))
			
			session['uploaded_data_file_path'] = os.path.join(placement, data_filename)
			#droptable = 'DROP TABLE IF EXISTS '
			#cur.execute(droptable+tablename)
			create = "CREATE TABLE (id SERIAL PRIMARY KEY, unique_id INT, tectonic_set VARCHAR(150), location VARCHAR(1000), rock_name VARCHAR(150), material VARCHAR(150), rock_type VARCHAR(150), siO2 FLOAT, al2o3 FLOAT, caO FLOAT, na2O FLOAT, k2O FLOAT, feO FLOAT, fe2O3 FLOAT, feO_total FLOAT, mgO FLOAT, mnO FLOAT, p2O5 FLOAT, loss FLOAT);"
			
			cur.execute(create[:13]+tablename+create[12:])
			conn.commit()
			#cur.execute(f"CREATE TABLE {tablename} (id SERIAL PRIMARY KEY, unique_id INT, tectonic_set VARCHAR(150), location VARCHAR(1000), rock_name VARCHAR(150), material VARCHAR(150), rock_type VARCHAR(150), siO2 FLOAT, al2o3 FLOAT, caO FLOAT, na2O FLOAT, k2O FLOAT, feO FLOAT, fe2O3 FLOAT, feO_total FLOAT, mgO FLOAT, mnO FLOAT, p2O5 FLOAT, loss FLOAT);")
			parseCSV(session['uploaded_data_file_path'],tablename)

			os.remove(os.path.join(placement, data_filename)) # remove csv file from uploads folder 
			flash('Data successfully uploaded!', category='success')
			return render_template('upload.html')

	return render_template('upload.html')


def parseCSV(filePath, tablename):
	# CVS Column Names
	# Use Pandas to parse the CSV file
	csvData = pd.read_csv(filePath, usecols=cols, encoding='unicode_escape')
	csvData.dropna(subset='UNIQUE_ID',axis=0, inplace=True)
    # Loop through the Rows
	for index, row in csvData.iterrows():
		
		sql = "INSERT INTO (unique_id, tectonic_set, location, rock_name, material, rock_type, siO2, al2o3, caO, na2O, k2O, feO, fe2O3, feO_total, mgO, mnO, p2O5, loss) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
		values = (
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
		cur.execute(sql[:12]+tablename+sql[11:], values)
		conn.commit()
	return jsonify({})




@views.route("/query", methods=['GET','POST'])
def query():
	cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\';')
	conn.commit()
	tablelist = cur.fetchall()
	if request.method == 'GET':
		return render_template("query.html", tablelist=tablelist)
	if request.method == 'POST':

		table = request.form.get('table')
		flash(f'You chose table {table}', category='success')
		
		chemElm = request.form.get('chemElm')
		cur.execute(f'SELECT MAX({chemElm}) FROM {table} WHERE {chemElm} != \'NaN\' ;')
		conn.commit()
		maxChemElm = cur.fetchall()
		cur.execute(f'SELECT MIN({chemElm}) FROM {table} WHERE {chemElm} != \'NaN\' ;')
		conn.commit()
		minChemElm = cur.fetchall()

		selectCol = request.form.get('selectCol')
		cur.execute (f'SELECT DISTINCT {selectCol} FROM {table};')
		conn.commit()
		selectOutput = cur.fetchall()

		# create plots
		harkerdiagrams(table)
		image = table + '.png'

		return render_template("querysubmit.html", table=table, selectOutput=selectOutput, chemElm=chemElm, maxChemElm=maxChemElm, minChemElm=minChemElm, selectCol=selectCol, tablelist=tablelist, image=image)
	

@views.route("/querysubmit", methods=['GET','POST'])
def querysubmit():
	return render_template("querysubmit.html")


@views.route("/tables", methods=['GET','POST'])
def tables():
	cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\';')
	conn.commit()
	tablelist = cur.fetchall()
	return render_template("tables.html", tablelist=tablelist)

@views.route('/delete-table/<table>', methods=['GET'])
def delete_table(table):  
	print(table)
	cur.execute(f'DROP TABLE IF EXISTS {table};')
	conn.commit()
	return redirect("/tables")


# –––––– function to create harker diagrams –––––––
def harkerdiagrams(table):
    sql = 'SELECT mgo, sio2, feo_total, al2o3, cao, mno, p2o5 FROM ;'
    cur.execute(sql[:56]+table+sql[56:])

    conn.commit()

    q1 = cur.fetchall()


    elements = ['mgo', 'sio2', 'feo_total', 'al2o3', 'cao', 'mno', 'p2o5']
    df = pd.DataFrame(q1, columns=elements)


    # Set up 2x3 plots
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
    sub = [ax1, ax2, ax3, ax4, ax5, ax6]

    elements = ['mgo', 'sio2', 'feo_total', 'al2o3', 'cao', 'mno', 'p2o5']
    elements2 = ['sio2', 'feo_total', 'al2o3', 'cao', 'mno', 'p2o5']

    labels = [r'SiO$_2$ (wt%)', r'FeO$_T$ (wt%)', r'Al$_2$O$_3$ (wt%)', r'CaO (wt%)', r'MnO (wt%)',
                r'P$_2$O$_5$ (wt%)']
    symbolsDict = {'Vaigat': '^', 'Maligat': 'v', 'Kanisut': 'p', 'Hareoen': 'D', 'Delta': 'o'}
    coloursDict = {'Vaigat': '#7fc97f', 'Maligat': '#beaed4', 'Kanisut': '#fdc086',
                    'Hareoen': '#386cb0', 'Delta': '#f0027f'}
    titles = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)']

    x = df['mgo']
    for s in range(6):
        sub[s].plot(x, df[elements2[s]], symbolsDict['Delta'], markerfacecolor=coloursDict['Delta'],
                                    markeredgecolor='black', markersize=4, label=table)

        sub[s].set_xlabel('MgO (wt%)')
        sub[s].set_ylabel(labels[s])
        sub[s].legend(numpoints=1, fontsize=6)
        sub[s].set_title(titles[s], x=-0.1, y=1.05)

    plt.tight_layout()

    fig.set_size_inches(8, 6)
    img_placement = 'website/'+str(IMAGE_FOLDER)
    name = table + '.png'
    plt.savefig(os.path.join(img_placement,name),dpi=300, bbox_inches='tight', pad_inches=0.25)