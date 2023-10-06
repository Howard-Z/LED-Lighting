import requests
import json
from sandbox import *
import time
# Replace these with your WLED device's information
wled_ip = "192.168.1.121"  # Replace with your WLED device's IP address

# URL for the WLED JSON API
api_url = f"http://{wled_ip}/json"

# Create a dictionary to toggle the power state
power_toggle = {
    "on": {
        "on": True
    },
    "off": {
        "on": False
    }
}

# Function to toggle WLED on or off
def toggle_wled_power(state):
    try:
        # Send a POST request to change the power state
        eff = Effect("192.168.1.121")
        eff.transmit(state)
        #data=json.dumps(state)


    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Toggle WLED on
toggle_wled_power(power_toggle["on"])

# Toggle WLED off
#toggle_wled_power(power_toggle["off"])

# test = {"seg":{"i":["FF0000"]}}
# toggle_wled_power(test)

eff = Wipe("192.168.1.121", 0, 329, 10, True, 200)
while(eff.status != True):
    eff.generateFrame()
    eff.transmit()
    time.sleep(1/2)
