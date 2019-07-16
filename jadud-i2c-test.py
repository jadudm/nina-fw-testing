import board
import busio
from digitalio import DigitalInOut
import config
import time

# Using the new I2C library.
import adafruit_esp32spi.adafruit_esp32spi_requests as requests

from adafruit_esp32i2c import adafruit_esp32

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "http://api.coindesk.com/v1/bpi/currentprice/USD.json"

params = {'SCL' : board.SCL, 'SDA' : board.SDA, 'address' : 0x2A}
protocol = adafruit_esp32.I2C(params, 
                              ready_pin=DigitalInOut(board.D5), 
                              reset_pin=DigitalInOut(board.D6),
                              debug=True)

esp = adafruit_esp32.ESP_Control(protocol)
requests.set_interface(esp)

print("ESP32 I2C webclient test")

if esp.status == adafruit_esp32.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")

print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])

#for ap in esp.scan_networks():
#    print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi']))


print("Connecting to AP...")
time.sleep(1)
# esp.connect_AP("phnphn", "nutnutnut")
esp.connect_AP(config.ssid, config.password)
time.sleep(5)

while not esp.is_connected:
    try:
        esp.connect_AP(config.ssid, config.password)
        time.sleep(5)
    except RuntimeError as e:
        print("could not connect to AP, retrying: ",e)
        continue

print("Connected to", str(esp.ssid, 'utf-8'), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))
print("IP lookup adafruit.com: %s" % esp.pretty_ip(esp.get_host_by_name("adafruit.com")))
print("Ping google.com: %d ms" % esp.ping("google.com"))

#esp._debug = True
print("Fetching text from", TEXT_URL)
r = requests.get(TEXT_URL)
print('-'*40)
print(r.text)
print('-'*40)
r.close()

print()
print("Fetching json from", JSON_URL)
r = requests.get(JSON_URL)
print('-'*40)
print(r.json())
print('-'*40)
r.close()

print("Done!")
