from flask import Blueprint

from suresol import db
from suresol.models import DangerLocation
from suresol.sos.forms import (DangerLocationsForm, SubmitBatterySOSForm,
                               SubmitDeleteBatterySOSForm, SubmitSOSForm)
from suresol.sos.utils import add_task, remove_task, send_sos_wa

sos = Blueprint('sos', __name__)

@sos.route("/send_sos", methods=['POST'])
def send_sos():
    form = SubmitSOSForm()
    if form.validate_on_submit():
        for contact in form.emergency_nums.data:
            send_sos_wa(form.user_name.data, contact, form.lat.data, form.lon.data)
        locationRecord = DangerLocation(lat=form.lat.data, lon=form.lon.data) # type: ignore
        db.session.add(locationRecord)
        db.session.commit()
        return {"message": "SOS sent successfully"}, 200
    return {"error": "Bad Request"}, 400


@sos.route("/get_danger_locations", methods=['GET'])
def get_danger_locations():
    form = DangerLocationsForm()
    if form.validate_on_submit():
        lat, lon = form.lat.data, form.lon.data
        dangerLocations = DangerLocation.query.filter(
            DangerLocation.lat.between(lat-0.01, lat+0.01), # type: ignore
            DangerLocation.lat.between(lon-0.01, lon+0.01) # type: ignore
        ).all()
        return {
            "message": "Danger locations fetched successfully" if dangerLocations else "No danger locations found",
            "data": [f"{location.lat},{location.lon}" for location in dangerLocations]
        }, 200
    return {"error": "Bad Request"}, 400

@sos.route("/schedule_battery_sos", methods=['POST'])
def schedule_battery_sos():
    form = SubmitBatterySOSForm()
    if form.validate_on_submit():
        task_id = add_task(form.user_name.data, form.emergency_nums.data, form.lat.data, form.lon.data)
        return {"message": "SOS scheduled successfully", "task_id": task_id}, 200
    return {"error": "Bad Request"}, 400

@sos.route("/delete_battery_sos", methods=['POST'])
def delete_battery_sos():
    form = SubmitDeleteBatterySOSForm()
    if form.validate_on_submit():
        r = remove_task(form.task_id.data)
        if r:         
            return {"message": "SOS deleted successfully"}, 200
        return {"error": "Invalid task ID"}, 404
    return {"error": "Bad Request"}, 400

