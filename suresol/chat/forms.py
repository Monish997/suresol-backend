from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ChatForm(FlaskForm):
    class Meta:
        csrf = False
    
    message = StringField('Message')
    

