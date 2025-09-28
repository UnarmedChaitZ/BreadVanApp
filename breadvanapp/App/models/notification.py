from App.database import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"))

def __repr__(self):
    return f"<Notification to Resident {self.resident_id}: {self.message}>"