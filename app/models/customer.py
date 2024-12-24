from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(256))
    id_number = db.Column(db.String(18))  # 身份证号
    created_at = db.Column(db.DateTime, default=db.func.now()) 