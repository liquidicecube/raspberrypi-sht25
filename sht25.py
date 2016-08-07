#!/usr/bin/python -u

import sys, time
import httplib, urllib

sys.path.append('../sht21_python')
from sht21 import SHT21

i2cBus                  = 1
thingspeak_url          = "api.thinkspeak.com"
thingspeak_api_key      = "VTJZEP5XT2TRVJCX"
sampleDelaySecs         = 300

# alerts
alertHumidityMin        = 30
alertHumidityMax        = 50
alertTemperatureMin     = 67
alertTemperatureMax     = 72

sht21Sensor = SHT21(i2cBus)
while True:
    print time.ctime()

    tempCelsius = sht21Sensor.read_temperature()
    tempFarenheit = tempCelsius * 9.0 / 5 + 32
    print "Temperature: %.2f degrees farenheit" % tempFarenheit

    humidityPercent = sht21Sensor.read_humidity()
    print "Humidity: %.2f" % humidityPercent

    params = urllib.urlencode({'field1': tempFarenheit,
                               'field2': humidityPercent,
                               'key':    thingspeak_api_key})
    #headers = {"Content-type": "application/x-www-form-urlencoded",
    #               "Accept":  "text/plain"}
    #conn = httplib.HTTPConnection(thingspeak_url)
    #conn.request("POST", "/update", params, headers)
    #conn.request("GET", "/update?%s" % params, params)
    #response = conn.getresponse()
    #print response.status, response.reason
    #data = response.read()

    f = urllib.urlopen("http://api.thingspeak.com:80/update?%s" % params)
    print f.read()

    time.sleep(sampleDelaySecs)
