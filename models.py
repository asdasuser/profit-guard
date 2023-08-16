from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ChargeClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    agree_terms = db.Column(db.Boolean, default=False)
    agree_age = db.Column(db.Boolean, default=False)
    fraud_type = db.Column(db.String(50))
    lost_amount = db.Column(db.String(50))
    contact_method = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    upload_status = db.Column(db.Boolean, default=False)
    
    
    def __init__(self, name, email, phone,
                agree_terms=False, agree_age=False,
                fraud_type=None, lost_amount=None,
                contact_method=None
        ):
        self.name = name
        self.email = email
        self.phone = phone
        self.agree_terms = agree_terms
        self.agree_age = agree_age
        self.fraud_type = fraud_type
        self.lost_amount = lost_amount
        self.contact_method = contact_method

    
    
    def __repr__(self):
        return f"<ChargeClient(id={self.id}, name={self.name}, email={self.email}, timestamp={self.timestamp}, upload_status={self.upload_status})>"

    def mark_as_uploaded(self):
        self.upload_status = True

    def format_info(self):
        return (
        f"Fraud Type: {self.fraud_type}\n"
        f"Lost Amount: {self.lost_amount}\n"
        f"Name: {self.name}\n"
        f"Phone: {self.phone}\n"
        f"Email: {self.email}\n"
        f"Contact Method: {self.contact_method}\n"
        f"Timestamp: {self.timestamp}"
    )

    @classmethod
    def get_all_records(cls):
        return cls.query.all()
    

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_method = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    agree_terms = db.Column(db.Boolean, nullable=False)
    agree_age = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Boolean, default=False)
