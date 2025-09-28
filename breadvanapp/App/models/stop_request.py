from App.database import db
from .drive import Drive

class StopRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)
    street = db.Column(db.String(100))
    time = db.Column(db.String(50))
    status = db.Column(db.String(20), default="pending")

    driver = db.relationship("Driver", backref="stop_requests")
    resident = db.relationship("Resident", backref="stop_requests")

    def __repr__(self):
        return f"<StopRequest {self.id} from Resident {self.resident_id} to Driver {self.driver_id}, status={self.status}>"

    @classmethod
    def create_for_street(cls, resident_id, street, time):
        """Create a stop request and link it to an existing drive if available"""
        drive = Drive.query.filter_by(street=street).first()
        
        stop_request = cls(
            resident_id=resident_id,
            driver_id=drive.driver_id if drive else None,
            street=street,
            time=time,
            status="scheduled" if drive else "pending"
        )
        
        db.session.add(stop_request)
        db.session.commit()
        return stop_request

    @classmethod
    def get_pending_for_street(cls, street):
        """Get all pending stop requests for a street"""
        return cls.query.filter_by(street=street, status="pending").all()

    def assign_driver(self, driver_id, time):
        """Assign a driver to this stop request"""
        self.driver_id = driver_id
        self.time = time
        self.status = "scheduled"
        db.session.commit()
