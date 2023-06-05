from . import db
from sqlalchemy.sql import func

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = 'UNIQUE_ID'
    tectonic_set = 'TECTONIC SETTING'
    location = 'LOCATION'
    rock_name =  'ROCK NAME'
    material = 'MATERIAL'
    rock_type = 'ROCK TYPE'
    siO2 = 'SIO2(WT%)'
    al2o3 = 'AL2O3(WT%)'
    caO =  'CAO(WT%)'
    na2O3 = 'NA2O(WT%)'
    k2O = 'K2O(WT%)'
    feO = 'FEO(WT%)'
    fe2O3 = 'FE2O3(WT%)'
    feO_total = 'FEOT(WT%)'
    mgO = 'MGO(WT%)'
    mnO = 'MNO(WT%)'
    p2O5 = 'P2O5(WT%)'
    loss = 'LOI(WT%)'
