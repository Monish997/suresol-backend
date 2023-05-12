import os
from datetime import datetime
from random import choices

from flask import Blueprint

from suresol import db, tw_client
from suresol.models import OTPRecord
from suresol.otp.forms import SendOTPForm, VerifyOTPForm

otp = Blueprint('otp', __name__)

@otp.route('/otp/send', methods=['POST'])
def send_otp():
    form = SendOTPForm()
    if form.validate_on_submit():
        _otp = ''.join(choices('0123456789', k=5))
        message = f"Hello {form.person_name.data}. Welcome to {form.company_name.data}. Your OTP for registration is: {_otp}"
        tw_client.messages.create(body=message, from_=os.environ.get("TWILIO_SMS_NUMBER", ""), to=form.mobile_num.data)
        otp_record = OTPRecord(phone_number=form.mobile_num.data, otp=_otp)
        db.session.add(otp_record)
        db.session.commit()
        return {"message": "OTP sent successfully"}, 200
    return {"error": "Bad Request"}, 400

@otp.route('/otp/verify', methods=['POST'])
def verify_otp():
    form = VerifyOTPForm()
    if form.validate_on_submit():
        otp_record = OTPRecord.query.filter(
            (OTPRecord.phone_number == form.mobile_num.data) 
            & (OTPRecord.valid_till > datetime.utcnow())
        ).order_by(OTPRecord.time.desc()).first()
        for r in OTPRecord.query.all():
            print(r.phone_number, r.otp, r.time, r.valid_till)
        if otp_record and otp_record.otp == form.otp.data:
            query = OTPRecord.__table__.delete().where(OTPRecord.phone_number == form.mobile_num.data)
            db.session.execute(query)
            db.session.commit()
            return {"message": "OTP verified successfully"}, 200
        return {"error": "Invalid OTP"}, 404
    return {"error": "Bad Request"}, 400



