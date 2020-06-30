import threading
from time import sleep
from gpiozero import DigitalInputDevice
import math
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connetion Retruned Code=", rc)

MQTT_SERVER_IP = "192.168.1.136"
MQTT_CLIENT_NAME = "weather"
MQTT_TOPIC = "domoticz/in"
RAIN_DOMOTICZ_ID = 68
TEMP_DOMOTICZ_ID = 67
WIND_DOMOTICZ_ID = 69

mqtt_c = mqtt.Client(MQTT_CLIENT_NAME)
mqtt_c.on_connect = on_connect
print("Connecting to MQTT server")
mqtt_c.connect(MQTT_SERVER_IP)
mqtt_c.loop_start()

dia_m = 0.18
bucket_count = 0
wind_count = 0
rain_cum = 0
interval = 4
ADJUSTMENT = 1.18 * (interval / 5)
BUCKET_SIZE = 0.2794

circ_m = dia_m * math.pi
wind_speed_sensor = DigitalInputDevice(17, pull_up=True)
temp_sensor = W1ThermSensor()
rain_sensor = DigitalInputDevice(27, pull_up=True)


def wind(time_sec):
    global wind_count
    rotations = wind_count / 2.0
    dist_m = circ_m * rotations
    m_per_sec = (dist_m / time_sec) * ADJUSTMENT
    wind_count = 0
    return m_per_sec


def spin():
    global wind_count
    wind_count = wind_count + 1


def rain():
    global rain_cum
    rain_cum = rain_cum + BUCKET_SIZE


def temperature():
    return temp_sensor.get_temperature()


windspeed = threading.Thread(name="wind", target=wind(interval))
raindata = threading.Thread(name="rain", target=rain)
windspeed.start()
raindata.start()
wind_speed_sensor.when_activated = spin
rain_sensor.when_activated = rain
speed = []
i = 0
while True:
    sleep(interval)
    speed.append(wind(interval))
    i += 1
    if i == 15:
        temper = temperature()
        speed_avg = sum(speed, 0.00) / len(speed)
        speed_gust = max(speed)

        payload = json.dumps(
            {
                "idx": RAIN_DOMOTICZ_ID,
                "nvalue": 0,
                "svalue": "{rain_cum};{rain_cum}".format(**locals()),
            }
        )
        mqtt_c.publish(MQTT_TOPIC, payload)

        #print("Publish data: " + payload)

        payload = json.dumps(
            {
                "idx": TEMP_DOMOTICZ_ID,
                "nvalue": 0,
                "svalue": "{temper}".format(**locals()),
            }
        )
        mqtt_c.publish(MQTT_TOPIC, payload)

        #print("Publish data: " + payload)
        temper_windchill = temper - (speed_avg * 0.7)
        payload = json.dumps(
            {
                "idx": WIND_DOMOTICZ_ID,
                "nvalue": 0,
                "svalue": "0;S;{speed_avg}*10;{speed_gust}*10;{temper};{temper_windchill}".format(**locals()),
            }
        )
        mqtt_c.publish(MQTT_TOPIC, payload)

        #print("Publish data: " + payload)

        i = 0
        speed.clear()
    else:
        pass

