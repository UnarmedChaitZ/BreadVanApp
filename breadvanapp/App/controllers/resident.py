from App.models import Resident

# Simple proxy methods that delegate to the model
def view_inbox(resident_name):
    resident = Resident.get_by_name(resident_name)
    if resident:
        return resident.view_inbox()
    return []

def request_stop(resident_name, driver_name):
    resident = Resident.get_by_name(resident_name)
    if resident:
        return resident.request_stop(driver_name)
    return None

def create_stop_request(resident_id, street, time):
    from App.models import StopRequest
    return StopRequest.create_for_street(resident_id, street, time)