from flask import Blueprint, render_template, request, flash, jsonify
#from . import db, app, UPLOAD_FOLDER
import json
from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from os import path
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import psycopg2

#with open('/Users/tove/Downloads/2023-06-KAIVCT_ANTARCTICA.csv') as f:
#    print(f)

"""cols = ['UNIQUE_ID','TECTONIC SETTING', 'LOCATION', 'ROCK NAME','MATERIAL','ROCK TYPE', 'SIO2(WT%)', 'AL2O3(WT%)', 'CAO(WT%)', 'NA2O(WT%)', 'K2O(WT%)', 'FEO(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)', 'MGO(WT%)', 'MNO(WT%)', 'P2O5(WT%)', 'LOI(WT%)']


data = pd.read_csv('/Users/tove/Downloads/2023-06-KAIVCT_ANTARCTICA.csv',usecols=cols,encoding='unicode_escape')
data.dropna(subset='UNIQUE_ID',axis=0, inplace=True)

#print(data)

for index,row in data.iterrows():
    print (data['LOCATION'][row])"""



"""new_sample = Sample(unique_id = row['UNIQUE_ID'], 
							tectonic_set = row['TECTONIC SETTING'],
    						location = row['LOCATION'],
    						rock_name = row['ROCK NAME'],
							material = row['MATERIAL'],
							rock_type = row['ROCK TYPE'],
							siO2 = (i,row['SIO2(WT%)'],
							al2o3 = (i,row['AL2O3(WT%)']),
							caO = (i,row['CAO(WT%)']),
							na2O = (i,row['NA2O(WT%)']),
							k2O = (i,row['K2O(WT%)']),
							feO = (i,row['FEO(WT%)']),
							fe2O3 = (i,row['FE2O3(WT%)']),
							feO_total = (i,row['FEOT(WT%)']),
							mgO = (i,row['MGO(WT%)']),
							mnO = (i,row['MNO(WT%)']),
							p2O5 = (i,row['P2O5(WT%)']),
							loss = (i,row['LOI(WT%)']))"""





conn = psycopg2.connect(host="localhost", user="postgres", dbname="dis2023", password="wildeisfine",port="5432")
cur = conn.cursor()

"""try: 
	q1 = cur.execute('SELECT sio2 FROM iceland;')
	if cur.fetchall():
		print('YAY')
except: print('NO')"""

"""check = 'SELECT * FROM ;'
print(check[:14]+'iceland'+check[14:])
cur.execute(check[:14]+'iceland'+check[14:])
if cur.fetchone():
	print('yay')"""

#create = "CREATE TABLE (id SERIAL PRIMARY KEY, unique_id INT, tectonic_set VARCHAR(150), location VARCHAR(1000), rock_name VARCHAR(150), material VARCHAR(150), rock_type VARCHAR(150), siO2 FLOAT, al2o3 FLOAT, caO FLOAT, na2O FLOAT, k2O FLOAT, feO FLOAT, fe2O3 FLOAT, feO_total FLOAT, mgO FLOAT, mnO FLOAT, p2O5 FLOAT, loss FLOAT);"
#print(create[:13]+'hej'+create[12:])

#create = "CREATE TABLE (id SERIAL PRIMARY KEY, unique_id INT, tectonic_set VARCHAR(150), location VARCHAR(1000), rock_name VARCHAR(150), material VARCHAR(150), rock_type VARCHAR(150), siO2 FLOAT, al2o3 FLOAT, caO FLOAT, na2O FLOAT, k2O FLOAT, feO FLOAT, fe2O3 FLOAT, feO_total FLOAT, mgO FLOAT, mnO FLOAT, p2O5 FLOAT, loss FLOAT);"
			
#cur.execute(create[:13]+'TEST2'+create[12:])
#conn.commit()


# get the table names
#q2 = cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\';')
#conn.commit()
#print(cur.fetchall())

cur.execute('SELECT MAX(sio2) FROM sample WHERE sio2 != \'NaN\' ;')
conn.commit()

print(cur.fetchall())



text = 'hej med dig'
text = text.replace(' ', '-')
print(text)