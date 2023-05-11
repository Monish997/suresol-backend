from flask_wtf import FlaskForm
from wtforms import Field, FloatField, StringField
from wtforms.validators import InputRequired, NumberRange


class ListField(Field):
    def process_formdata(self, valuelist):
        self.data = valuelist


class SubmitSOSForm(FlaskForm):
    class Meta:
        csrf = False

    user_name = StringField("Name", validators=[InputRequired()])
    lat = FloatField("Latitude", validators=[InputRequired(), NumberRange(-90, 90)])
    lon = FloatField("Longitude", validators=[InputRequired(), NumberRange(-180, 180)])
    emergency_nums = ListField("Emergency numbers", validators=[InputRequired()])


class SubmitBatterySOSForm(FlaskForm):
    class Meta:
        csrf = False

    user_name = StringField("Name", validators=[InputRequired()])
    lat = FloatField("Latitude", validators=[InputRequired(), NumberRange(-90, 90)])
    lon = FloatField("Longitude", validators=[InputRequired(), NumberRange(-180, 180)])
    emergency_nums = ListField("Emergency numbers", validators=[InputRequired()])

    

class SubmitDeleteBatterySOSForm(FlaskForm):
    class Meta:
        csrf = False

    task_id = StringField("Task ID", validators=[InputRequired()])

    

class DangerLocationsForm(FlaskForm):
    lat = FloatField("Latitude", validators=[InputRequired(), NumberRange(-90, 90)])
    lon = FloatField("Longitude", validators=[InputRequired(), NumberRange(-180, 180)])
    
