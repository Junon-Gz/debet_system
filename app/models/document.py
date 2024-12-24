from app import db
from datetime import datetime

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debt_id = db.Column(db.Integer, db.ForeignKey('debt.id'))
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    debt = db.relationship('Debt', backref='documents') 