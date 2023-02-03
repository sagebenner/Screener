from main import db

class DSQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fatigue = db.Column(db.Integer)
    minex = db.Column(db.Integer)
    unrefreshed = db.Column(db.Integer)
    remember = db.Column(db.Integer)
