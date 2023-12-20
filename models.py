from db import db

class Upload(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    filename=db.Column(db.String(50))
    data=db.Column(db.LargeBinary)