from App.models import Driver

# Simple proxy methods that delegate to the model
def schedule_drive(driver_name, street, time):
    driver = Driver.get_by_name(driver_name)
    if driver:
        return driver.schedule_drive(street, time)
    return None

def get_driver_status(driver_name):
    driver = Driver.get_by_name(driver_name)
    if driver:
        return driver.get_status()
    return None

def get_all_drivers():
    return Driver.get_all()

def update_location(driver_name, new_location):
    driver = Driver.get_by_name(driver_name)
    if driver:
        return driver.update_location(new_location)
    return False


    