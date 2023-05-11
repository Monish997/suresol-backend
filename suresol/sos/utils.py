import os
from datetime import timedelta
from secrets import token_hex

from suresol import scheduler, tw_client

BATTERY_DELAY = timedelta(hours=10)
tasks = {}

def send_sos_wa(name, contact, lat, lon):
    locationLink = f"http://maps.google.com/maps?z=18&q={lat},{lon}"
    msgBody = f"{name} is in emergency and requires your help. Please reach out to them at the following location: {locationLink}"
    _ = tw_client.messages.create(
        body=msgBody,
        from_="whatsapp:" + os.environ.get("TWILIO_WA_NUMBER"),  # type: ignore
        to="whatsapp:+91" + contact,
    )


def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ("year", 60 * 60 * 24 * 365),
        ("month", 60 * 60 * 24 * 30),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1),
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = "s" if period_value > 1 else ""
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return " ".join(strings)


def add_task(name, contacts, lat, lon):
    locationLink = f"http://maps.google.com/maps?z=18&q={lat},{lon}"
    msgBody = f"{name}'s battery ran out {td_format(BATTERY_DELAY)} ago. Last known location: {locationLink}"
    taskID = token_hex(16)
    tasks[taskID] = {"time": BATTERY_DELAY.total_seconds(), "contacts": contacts, "body": msgBody}
    return taskID


def report_battery():
    to_execute = []
    with scheduler.app.app_context(): # type: ignore
        for key, value in tasks.items():
            if value["time"] <= 0:
                to_execute.append(key)
                continue
            tasks[key]["time"] -= scheduler.app.config["JOBS"][0]["seconds"] # type: ignore
    for key in to_execute:
        for contact in tasks[key]["contacts"]:
            tw_client.messages.create(
                to="whatsapp:+91"+contact,
                from_="whatsapp:"+os.environ["TWILIO_WA_NUMBER"],
                body=tasks[key]["body"],
            )
        del tasks[key]


def remove_task(taskID):
    if taskID in tasks:
        del tasks[taskID]
        return True
    return False
