## Description

This is a python script for the Makerlife Weatherstation to push data via MQTT to Domoticz. Is is base on github:kobbas/mqttweather.
It will publish temperature, rain and wind values on the domoticz/in topic. 

The data is pushed every 5 min. The time to can be changed if the INTERVAL variable is changed. The wind measurement is done during the interval seconds. Each publish consists of 15 measurement rounds.

Wind direction is not measured only dummy values a are sent.

### Things you need to do to get it working.

Paho Mqtt has to be added to your python installation. 

`pip install paho-mqtt`

Edit the script with your MQTT broker IP. No pass is used.
```
MQTT_SERVER_IP = "192.168.1.x"
```

Update the IDs to match the idx in Domoticz for the devices.
```
RAIN_DOMOTICZ_ID = 68
TEMP_DOMOTICZ_ID = 67
WIND_DOMOTICZ_ID = 69
```
For setting up Domiticz for MQTT look here ["MQTT Client Gateway"](https://www.domoticz.com/wiki/MQTT#Add_hardware_.22MQTT_Client_Gateway.22)

Login to the you raspi via SSH. Start the script with:

`nohup python weather.py &`

This enables to logout from the pi without closing the down the script.
