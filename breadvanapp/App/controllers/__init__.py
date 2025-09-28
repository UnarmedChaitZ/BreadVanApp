from .user import *
from .auth import *
from .driver import Driver
from .resident import Resident
from .initialize import *
from App.database import db
from App.models.driver import Driver
from App.models.resident import Resident
from App.models.drive import Drive
from App.models.stop_request import StopRequest

def initialize():
    """Initialize the database with sample data"""
    # Clear existing data
    StopRequest.query.delete()
    Drive.query.delete()
    Resident.query.delete()
    Driver.query.delete()
    db.session.commit()

    # Sample Drivers
    drivers = [
        Driver(name="John", current_location="Main Street", status="available"),
        Driver(name="Alice", current_location="High Street", status="available"),
        Driver(name="Bob", current_location="Downtown", status="available"),
        Driver(name="Eve", current_location="Uptown", status="available"),
    ]
    db.session.add_all(drivers)
    db.session.commit()

    # Sample Residents
    residents = [
        Resident(name="Mary", street="Main Street"),
        Resident(name="Tom", street="High Street"),
        Resident(name="Lucy", street="Main Street"),
        Resident(name="Jack", street="High Street"),
    ]
    db.session.add_all(residents)
    db.session.commit()

    # Sample Drives
    drives = [
        Drive(driver_id=1, street="Main Street", time="18:00"),
        Drive(driver_id=2, street="High Street", time="19:00"),
    ]
    db.session.add_all(drives)
    db.session.commit()

    # Sample Stop Requests
    stop_requests = []
    for resident in residents:
        drives_on_street = Drive.query.filter_by(street=resident.street).all()
        for drive in drives_on_street:
            driver = drive.driver  # get driver
            if not driver:
                continue

            stop_request = StopRequest(
                driver_id=driver.id,
                resident_id=resident.id,
                street=resident.street,
                time=drive.time,
                status="pending"
            )
            stop_requests.append(stop_request)

            # mark driver busy
            if driver.status == "available":
                driver.status = "busy"

    db.session.add_all(stop_requests)
    db.session.commit()

    return drivers, residents









