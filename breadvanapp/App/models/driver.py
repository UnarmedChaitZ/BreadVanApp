from App.database import db
from .drive import Drive

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    current_location = db.Column(db.String(200))
    drives = db.relationship("Drive", backref="driver", lazy=True)
    status = db.Column(db.String(20), default="available")  # e.g., available, on route, off duty

    def __repr__(self):
        return f"<Driver {self.name}, Status: {self.status}, Location: {self.current_location}>"

    @classmethod
    def get_by_name(cls, driver_name):
        return cls.query.filter_by(name=driver_name).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def schedule_drive(self, street, time):
        """Schedule a drive for this driver"""
        self.current_location = street
        self.status = "busy"
        
        new_drive = Drive(driver_id=self.id, street=street, time=time)
        db.session.add(new_drive)
        db.session.commit()
        return new_drive

    def update_location(self, new_location):
        """Update driver's current location"""
        self.current_location = new_location
        db.session.commit()
        return True

    def update_status(self, new_status):
        """Update driver's status"""
        self.status = new_status
        db.session.commit()
        return True

    def get_status(self):
        """Get driver's current status and location"""
        return {
            "name": self.name,
            "status": self.status,
            "location": self.current_location
        }

    @classmethod
    def create(cls, driver_name, location="Warehouse", status="available"):
        """Create a new driver"""
        driver = cls(name=driver_name, current_location=location, status=status)
        db.session.add(driver)
        db.session.commit()
        return driver
