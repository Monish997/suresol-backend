from datetime import datetime, timedelta

from suresol import db


class DangerLocation(db.Model): # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lat = db.Column(db.Float, nullable=False, index=True)
    lon = db.Column(db.Float, nullable=False, index=True)


class OTPRecord(db.Model): # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False, index=True)
    otp = db.Column(db.String(6), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valid_till = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(minutes=10))