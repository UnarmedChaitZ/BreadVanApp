from App.database import db

class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(10), nullable=False)

def __repr__(self):
    return f"<Drive by Driver {self.driver_id} on {self.street} at {self.time}>"
    