from flask import Blueprint, render_template, request, flash, jsonify
#from . import db, app, UPLOAD_FOLDER
#from . import IMAGE_FOLDER
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
import matplotlib.pyplot as plt

IMAGE_FOLDER = os.path.join('staticFiles', 'images')
conn = psycopg2.connect(host="localhost", user="postgres", dbname="dis2023", password="wildeisfine",port="5432")
cur = conn.cursor()


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
    #plt.savefig(name, dpi=300, bbox_inches='tight', pad_inches=0.25)


harkerdiagrams('test1')
#print(len('SELECT mgo, sio2, feo_total, al2o3, cao, mno, p2o5 FROM ;'))
#sql = 'SELECT mgo, sio2, feo_total, al2o3, cao, mno, p2o5 FROM ;'
#print(sql[:56]+'sample'+sql[56:])