from App.database import db
from App.models.driver import Driver
from App.models.resident import Resident
from App.models.drive import Drive
from App.models.stop_request import StopRequest
from App.models.notification import Notification

def initialize():
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()
    db.session.commit()

