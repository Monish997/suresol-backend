from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client

from suresol.config import Config

db = SQLAlchemy()
scheduler = APScheduler()
tw_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()        

    from suresol.chat.routes import chat
    from suresol.sos.routes import sos

    app.register_blueprint(sos)
    app.register_blueprint(chat)

    return app
