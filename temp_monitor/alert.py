import requests                 # for making HTTP requests
import json                     # library for handling JSON data
import time                     # module for sleep operation

from boltiot import Bolt        # importing Bolt from boltiot module
import conf                     # config file

threshold = 30                  # threshold limit

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)

def get_sensor_value_from_pin(pin):
    """Returns the sensor value. Returns -999 if request fails"""
    try:
        response = mybolt.analogRead(pin)
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data)
            return -999
        sensor_value = int(data["value"])
        return sensor_value
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999

def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": conf.telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "GET",
            url,
            params=data
        )
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False

while True:
    # Step 1
    sensor_value = get_sensor_value_from_pin("A0")
    temp=(100*int(sensor_value))/1024
    print("The current temperature is:", str(temp))
    
    # Step 2
    if sensor_value == -999:
        print("Request was unsuccessfull. Skipping.")
        time.sleep(10)
        continue
    
    # Step 3
    if temp >= threshold:
        print("Sensor value has exceeded threshold")
        message = "Alert! temperature has exceeded " + str(conf.threshold) + \
                  ". The temperature is " + str(temp)
        telegram_status = send_telegram_message(message)
        print("This is the Telegram status:", telegram_status)

    # Step 4
    time.sleep(10)