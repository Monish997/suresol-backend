from flask_wtf import FlaskForm
from wtforms import StringField


class SendOTPForm(FlaskForm):
    class Meta:
        csrf = False
    
    mobile_num = StringField('Mobile Number')
    person_name = StringField('Person Name')
    company_name = StringField('Company Name')
    

class VerifyOTPForm(FlaskForm):
    class Meta:
        csrf = False
    
    mobile_num = StringField('Mobile Number')
    otp = StringField('OTP')

