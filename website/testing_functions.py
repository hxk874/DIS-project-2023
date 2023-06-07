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

#with open('/Users/tove/Downloads/2023-06-KAIVCT_ANTARCTICA.csv') as f:
#    print(f)

cols = ['UNIQUE_ID','TECTONIC SETTING', 'LOCATION', 'ROCK NAME','MATERIAL','ROCK TYPE', 'SIO2(WT%)', 'AL2O3(WT%)', 'CAO(WT%)', 'NA2O(WT%)', 'K2O(WT%)', 'FEO(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)', 'MGO(WT%)', 'MNO(WT%)', 'P2O5(WT%)', 'LOI(WT%)']


data = pd.read_csv('/Users/tove/Downloads/2023-06-KAIVCT_ANTARCTICA.csv',usecols=cols,encoding='unicode_escape')
data.dropna(subset='UNIQUE_ID',axis=0, inplace=True)

#print(data)

for index,row in data.iterrows():
    print (data['LOCATION'][row])



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



<div id="London" class="tabcontent">
      <h3>London</h3>
      <p>London is the capital city of England.</p>
    </div>