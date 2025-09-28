# BreadVanApp
A Flask application for managing bread van delivery routes and stop requests
# COMMANDS
```bash
[Database_Commands]
flask init                                              # Initialize database with sample data
flask print-data                                        # Print all database entries in tables

[Driver_Commands]
flask driver schedule-drive John "Main Street" "18:00"  # Schedule a drive for John to Main Street at 18:00
flask driver update-location Alice "High Street"        # Update Alice’s current location to High Street
flask driver view-status Bob                            # View Bob’s status and location
flask driver list-drivers                               # List all drivers in the database
flask driver update-status Eve available                # Update Eve’s status to 'available'
flask driver add-driver Charlie                         # Add a new driver named Charlie

[Resident_Commands]
flask resident view-inbox Mary                          # View inbox of stop requests for Mary’s street
flask resident request-stop Tom Alice                   # Tom requests a stop from Alice
flask resident view-driver-status Bob                   # View Bob’s status and location
flask resident list-residents                           # List all residents in the database
flask resident add-resident Linda "Downtown"            # Add a new resident named Linda on Downtown street
