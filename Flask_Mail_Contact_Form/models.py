# models.py
 
# SQLAlchemy Instance Is Imported
from init_db import db
 
# Declaring Model
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(35), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(1200), nullable=False)
    date = db.Column(db.String(12), nullable=True)
