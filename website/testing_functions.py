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

print(data)