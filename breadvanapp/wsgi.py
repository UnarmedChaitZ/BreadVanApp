import click, pytest, sys
from flask.cli import AppGroup

from App.database import db, get_migrate
from App.models import Driver
from App.models.resident import Resident
from App.models.stop_request import StopRequest
from App.models.drive import Drive
from App.main import create_app
from App.controllers import initialize
from App.controllers.driver import update_location, get_driver_status
from App.controllers.resident import view_inbox, request_stop, create_stop_request

from rich.console import Console
from rich.table import Table

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init_db():
    initialize()
    print("Database initialized with sample data!")


'''
Driver CLI commands

'''
driver_cli = AppGroup('driver', help='Driver object commands')

@driver_cli.command("schedule-drive", help="Schedule a drive to a street at a specific time")
@click.argument("driver_name")
@click.argument("street")
@click.argument("time")
def cli_schedule_drive(driver_name, street, time):
    driver = Driver.query.filter_by(name=driver_name).first()
    if not driver:
        print("Driver not found.")
        return

    # Update driver location and status
    driver.current_location = street
    driver.status = "busy"
    
    # Create a new drive entry
    new_drive = Drive(driver_id=driver.id, street=street, time=time)
    db.session.add(new_drive)
    db.session.commit()

    # Assign pending stop requests on this street at the specific time, only if not already assigned
    pending_stops = StopRequest.query.filter_by(street=street, status="pending").all()
    assignable_stops = [stop for stop in pending_stops if stop.driver_id is None]

    if not assignable_stops:
        print(f"No unassigned pending stop requests on {street} at {time}. Drive scheduled anyway.")
    else:
        for stop in assignable_stops:
            stop.driver_id = driver.id
            stop.time = time
            stop.status = "scheduled"
        db.session.commit()
        print(f"Assigned {len(assignable_stops)} stop request(s) to {driver.name}.")

    print(f"{driver.name} scheduled to {street} at {time}")



@driver_cli.command("update-location", help="Update driver's current location")
@click.argument("driver_name")
@click.argument("location")
def cli_update_location(driver_name, location):
    success = update_location(driver_name, location)
    if success:
        print(f"{driver_name}'s location updated to {location}")
    else:
        print("Driver not found.")

@driver_cli.command("view-status")
@click.argument("driver_name")
def cli_driver_status(driver_name):
    """Check the status of a driver."""
    status = get_driver_status(driver_name)
    if not status:
        print(f"Driver {driver_name} not found")
    else:
        name = status.get("name", "unknown")
        driver_status = status.get("status", "unknown")
        location = status.get("location", "main branch")
        print(f"Driver {name} is at {location} and his/her status is {driver_status}")


@driver_cli.command("list-drivers")
def list_drivers():
    from App.controllers.driver import get_all_drivers 
    drivers = get_all_drivers()
    if not drivers:
        print("No drivers found")
        return
    for driver in drivers:
        print(f"Name: {driver.name}, Status: {getattr(driver, 'status', 'unknown')}, Location: {getattr(driver, 'current_location', 'unknown')}")

#updates status of the driver
@driver_cli.command("update-status", help="Update driver's status")
@click.argument("driver_name")
@click.argument("status")
def cli_update_status(driver_name, status):
    driver = Driver.query.filter_by(name=driver_name).first()
    if driver:
        driver.status = status
        db.session.commit()
        print(f"{driver.name}'s status updated to {status}")
    else:
        print("Driver not found.")

#adds a new driver
@driver_cli.command("add-driver", help="Add a new driver")    
@click.argument("driver_name")
def cli_add_driver(driver_name):
    existing_driver = Driver.query.filter_by(name=driver_name).first()
    if existing_driver:
        print(f"Driver {driver_name} already exists.")
        return
    new_driver = Driver(name=driver_name, current_location="Warehouse", status="available")
    db.session.add(new_driver)
    db.session.commit()
    print(f"Driver {driver_name} added successfully.")


'''
Resident CLI commands

'''

resident_cli = AppGroup('resident', help='Resident object commands')

#use rich to display inbox in a table
@resident_cli.command("view-inbox", help="View inbox for scheduled drives to your street")
@click.argument("resident_name")
def cli_view_inbox(resident_name):
    from rich.table import Table
    from rich.console import Console
    from App.models.resident import Resident

    resident = Resident.query.filter_by(name=resident_name).first()
    if not resident:
        print(f"Resident {resident_name} not found.")
        return

    # Fetch all drives for the resident's street
    drives = Drive.query.filter_by(street=resident.street).all()
    if not drives:
        print(f"No scheduled drives found for {resident.street}.")
        return

    table = Table(title=f"{resident_name}'s Inbox - Scheduled Drives for {resident.street}")
    table.add_column("Driver", style="cyan")
    table.add_column("Street", style="magenta")
    table.add_column("Time", style="green")
    table.add_column("Status", style="yellow")

    for drive in drives:
        driver = Driver.query.get(drive.driver_id)
        driver_name = driver.name if driver else "Unassigned"
        table.add_row(driver_name, drive.street, drive.time, "scheduled")

    console = Console()
    console.print(table)


@resident_cli.command("request-stop", help="Request a stop from a driver")
@click.argument("resident_name")
@click.argument("driver_name")
def cli_request_stop(resident_name, driver_name):
    resident = Resident.query.filter_by(name=resident_name).first()
    driver = Driver.query.filter_by(name=driver_name).first()
    if not resident or not driver:
        print("Driver or resident not found.")
        return

    # Create a stop request
    stop_request = StopRequest(
        driver_id=driver.id,
        resident_id=resident.id,
        street=resident.street,
        time="18:00",
        status="completed"
    )
    db.session.add(stop_request)

    # Update driver status back to available
    driver.status = "available"
    db.session.commit()

    print(f"{resident_name} successfully requested a stop from {driver_name}")


@resident_cli.command("add-resident", help="Add a new resident")    
@click.argument("resident_name")
@click.argument("street")
def cli_add_resident(resident_name, street):
    from App.models.resident import Resident
    existing_resident = Resident.query.filter_by(name=resident_name).first()
    if existing_resident:
        print(f"Resident {resident_name} already exists.")
        return
    new_resident = Resident(name=resident_name, street=street)
    db.session.add(new_resident)
    db.session.commit()
    print(f"Resident {resident_name} added successfully.")


# Database commands - View all entries in the database
db_cli = AppGroup('print_data', help="Database related commands")

@app.cli.command("print-data", help="Print all database entries in tables")
def print_data():
    console = Console()

    # Drivers
    drivers = Driver.query.all()
    table = Table(title="Drivers")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Location", style="yellow")
    table.add_column("Status", style="magenta")
    for d in drivers:
        table.add_row(str(d.id), d.name, d.current_location, d.status)
    console.print(table)

    # Residents
    residents = Resident.query.all()
    table = Table(title="Residents")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Street", style="yellow")
    for r in residents:
        table.add_row(str(r.id), r.name, r.street)
    console.print(table)

    # Drives
    drives = Drive.query.all()
    table = Table(title="Drives")
    table.add_column("ID", style="cyan")
    table.add_column("Driver", style="green")
    table.add_column("Street", style="yellow")
    table.add_column("Time", style="magenta")
    for d in drives:
        driver = Driver.query.get(d.driver_id)
        driver_name = driver.name if driver else "Unassigned"
        table.add_row(str(d.id), driver_name, d.street, d.time)
    console.print(table)

    # Stop Requests
    stops = StopRequest.query.all()
    table = Table(title="Stop Requests")
    table.add_column("ID", style="cyan")
    table.add_column("Driver", style="green")
    table.add_column("Resident", style="yellow")
    table.add_column("Street", style="blue")
    table.add_column("Time", style="magenta")
    table.add_column("Status", style="red")
    for s in stops:
        driver_name = s.driver.name if s.driver else "Unassigned"
        resident_name = s.resident.name if s.resident else "Unknown"
        table.add_row(str(s.id), driver_name, resident_name, s.street, s.time, s.status)
    console.print(table)




app.cli.add_command(resident_cli) # add the group to the cli
app.cli.add_command(driver_cli) # add the group to the cli
app.cli.add_command(db_cli) # add the group to the cli


# testing
test = AppGroup('test', help='Testing commands')

@test.command("breadvan", help="Run Bread Van tests")
@click.argument("type", default="all")
def breadvan_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "BreadVanUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "BreadVanIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
