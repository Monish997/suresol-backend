import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

    JOBS = [
        {
            "id": "report_battery",
            "func": "sos.sos.utils:report_battery",
            "trigger": "interval",
            "seconds": 10,
        }
    ]
    SCHEDULER_API_ENABLED = False