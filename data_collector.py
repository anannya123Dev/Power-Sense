import random
from datetime import datetime

def get_api_data(device_master):
    """
    Generates simulated live readings for whatever devices are currently
    in device_master (a list of {"device": name, "wattage": watts} dicts).
    Devices can be added/removed at runtime via the /api/devices endpoints
    in app.py -- this function just reflects whatever list it's given.
    """
    devices = []
    for base in device_master:
        wattage = float(base["wattage"])
        voltage = 220 + random.uniform(-3, 3)
        # Derive current from wattage (P = V * I), matching how the
        # original fixed device list related current to its api_power.
        current = (wattage / 220.0) + random.uniform(-0.002, 0.002)
        devices.append({
            "device": base["device"],
            "voltage": voltage,
            "current": max(current, 0.001),
            "api_power": wattage,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return devices
