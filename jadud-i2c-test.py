import board
import busio
from digitalio import DigitalInOut
import config

# Using the new I2C library.
import adafruit_esp32spi.adafruit_esp32spi_requests as requests

from adafruit_esp32i2c import adafruit_esp32

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "http://api.coindesk.com/v1/bpi/currentprice/USD.json"

params = {'SCL' : board.SCL, 'SDA' : board.SDA, 'address' : 0x2A}
protocol = adafruit_esp32.I2C(params, ready_pin=DigitalInOut(board.D5), debug=3)

esp = adafruit_esp32.ESP_Control(protocol)
requests.set_interface(esp)

print("ESP32 I2C webclient test")

if esp.status == adafruit_esp32.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])

esp.set_digital_write(13, 1)
time.sleep(1)
esp.set_digital_write(13, 0)
time.sleep(1)

for ap in esp.scan_networks():
    print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi']))

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(config.ssid, config.password)
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
