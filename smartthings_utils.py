import requests
import time
import os
from dotenv import load_dotenv


connect_status_url = "https://api.smartthings.com/v1/devices/e68cde00-5ce0-4c0f-b32b-ba07410259a2/status"
turn_on_status_url = "https://api.smartthings.com/v1/devices/79c619ea-275f-4400-95a5-0f1212393805/status"

connect_url = "https://api.smartthings.com/v1/scenes/00a65550-a8db-40a2-977f-4c44906f2d4e/execute"
turn_on_url = "https://api.smartthings.com/v1/scenes/83fb0463-1641-482f-b7de-b334638b6aba/execute"

load_dotenv()

api_token = os.getenv("SMARTTHINGS_TOKEN")

headers = {
    "Authorization": "Bearer " + api_token
}

def get_status_connect():
    status = requests.get(connect_status_url, headers=headers)
    if (status.status_code != 200):
        print("failed connect status")
        return "failed"
    return status.json()["components"]["main"]["switch"]["switch"]["value"] 

def connect_pc():
    status = get_status_connect()

    if (status == "on"):
        print("already connected")
        return 0

    response = requests.post(connect_url, headers=headers)
    if (response.status_code == 200):
        print("done")
        return 1
    else:
        print("failed connect")
        return 2
    
def disconnect_pc():
    status = get_status_connect()

    if (status == "off"):
        print("already diconnected")
        return 0

    response = requests.post(connect_url, headers=headers)
    if (response.status_code == 200):
        print("done")
        return 1
    else:
        print("failed disconnect")
        return 2

def get_status_turn_on():
    status = requests.get(turn_on_status_url, headers=headers)
    if (status.status_code != 200):
        return "failed" 
    return (status.json()["components"]["main"]["healthCheck"]["DeviceWatch-DeviceStatus"]["value"], status.json()["components"]["main"]["switch"]["switch"]["value"])


def turn_on_pc():
    status = get_status_turn_on()

    while status[0] == "offline":
        print("status: " + status[0])
        if(connect_pc() == 2):
            return 2
        time.sleep(10)
        status = get_status_turn_on()
    print("status: " + status[0])


    if (status[1] == "on"):
        print("already turned on")
        return 0

    response = requests.post(turn_on_url, headers=headers)
    if (response.status_code == 200):
        print("turned on")
        return 1
    else:
        print("failed turned on")
        return 2

    

def turn_off_pc():
    status = get_status_turn_on()

    if (status[0] == "offline"):
        print("already turned off")
        return 0

    if (status[1] == "off"):
        print("already turned off")
        return 0

    while status [1] == "on":
        response = requests.post(turn_on_url, headers=headers)
        if (response.status_code == 200):
            print("turned off")
        else:
            print("failed turned off")
            return 2
        time.sleep(10)

        status = get_status_turn_on()
        print("turn on:"  + status[1])

    

    while status[0] != "offline":
        print("status: " + status[0])
        if(disconnect_pc() == 2):
            return 2
        time.sleep(10)
        status = get_status_turn_on()

    print("status: " + status[0])
