#!/usr/bin/python -u

import smbus
import time
import httplib, urllib
import email

deviceAddr = 0x40
measureTemperatureCmd   = 0xf3
measureTemperatureDelay = 0.100
measureHumidityCmd      = 0xf5
measureHumidityDelay    = 0.050
thingspeak_url          = "api.thinkspeak.com"
thingspeak_api_key      = "VTJZEP5XT2TRVJCX"
sampleDelaySecs         = 300

# alerts
alertHumidityMin        = 30
alertHumidityMax        = 50
alertTemperatureMin     = 67
alertTemperatureMax     = 72

# Sends byte opcode to device and measures 16-bit value
def measure(bus, addr, cmd, delay):
    bus.write_byte(addr, cmd)
    time.sleep(delay)
    msb = bus.read_byte(addr)
    lsb = bus.read_byte(addr)
    return(msb << 8) + lsb

bus = smbus.SMBus(1)
while True:
    print time.ctime()

    tempEncoded = measure(bus, deviceAddr, measureTemperatureCmd, measureTemperatureDelay)
    humidityEncoded = measure(bus, deviceAddr, measureHumidityCmd, measureHumidityDelay)

    tempCelsius = -46.85 + 175.72 * (float(tempEncoded) / 65536)
    tempFarenheit = round((tempCelsius * 9/5 + 32), 2)
    print "tempEncoded: {0}".format(tempEncoded)
    print "Temperature: {0} degrees farenheit".format(tempFarenheit)

    humidityPercent = round(-6 + 125 * (float(humidityEncoded) / 65536), 2)
    print "humidityEncoded: {0}".format(humidityEncoded)
    print "Humidity: {0}%".format(humidityPercent)


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
