
from App.database import db
from .stop_request import StopRequest
from .drive import Drive
from .driver import Driver

class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    street = db.Column(db.String(100))
    inbox = db.relationship("Notification", backref="resident", lazy=True)

    def __repr__(self):
        return f"<Resident {self.name} on {self.street}>"

    @classmethod
    def get_by_name(cls, resident_name):
        return cls.query.filter_by(name=resident_name).first()

    def view_inbox(self):
        """View all scheduled drives for resident's street"""
        drives = Drive.query.filter_by(street=self.street).all()
        inbox_items = []
        for drive in drives:
            driver = Driver.query.get(drive.driver_id)
            driver_name = driver.name if driver else "Unassigned"
            inbox_items.append({
                "driver_name": driver_name,
                "street": drive.street,
                "time": drive.time,
                "status": "scheduled"
            })
        return inbox_items

    def request_stop(self, driver_name):
        """Request a stop from a specific driver"""
        driver = Driver.query.filter_by(name=driver_name).first()
        if not driver:
            return None

        stop_request = StopRequest(
            resident_id=self.id,
            driver_id=driver.id,
            street=self.street,
            time="18:00",  # This could be made dynamic
            status="pending"
        )
        db.session.add(stop_request)
        db.session.commit()
        return stop_request

    @classmethod
    def create(cls, resident_name, street):
        """Create a new resident"""
        resident = cls(name=resident_name, street=street)
        db.session.add(resident)
        db.session.commit()
        return resident