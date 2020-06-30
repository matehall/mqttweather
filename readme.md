This is a python script for the Makerlife Weatherstation to push data via MQTT to Domoticz. Is is base on github:kobbas/mqttweather.
It will publish temperature, rain and wind values on the domoticz/in topic. 

The data is pushed every 5 min. The time to can be changed if the interval variable is changed. The wind measurement is done during the interval seconds. Each publish consists of 15 measurement rounds.

Things you need to do to get it working.

Paho Mqtt has to be added to your python installation. 

`pip install paho-mqtt` <br>

Edit the script with your MQTT broker IP and Pass.
```
MQTT_SERVER_IP = "192.168.1.136"
```

Update the IDs to match the idx in domoticz for the devices.
```
RAIN_DOMOTICZ_ID = 68
TEMP_DOMOTICZ_ID = 67
WIND_DOMOTICZ_ID = 69
```
For setting up MQTT for Domiticz look here ["MQTT Client Gateway"](https://www.domoticz.com/wiki/MQTT#Add_hardware_.22MQTT_Client_Gateway.22)

Login to the you raspi via SSH. Start the script with:<br>

`nohup python weather.py &`

This enables to logut from the pi without closing the down the script.
