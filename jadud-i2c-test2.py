import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
import config
import time

# Using the new I2C library.
import adafruit_esp32spi.adafruit_esp32spi_requests as requests
from adafruit_esp32i2c import adafruit_esp32

params = {'SCL' : board.SCL, 'SDA' : board.SDA, 'address' : 0x2A}
protocol = adafruit_esp32.I2C(params, 
                              ready_pin=DigitalInOut(board.D5), 
                              reset_pin=DigitalInOut(board.D6),
                              debug=3)

esp = adafruit_esp32.ESP_Control(protocol)
requests.set_interface(esp)

print("ESP32 I2C dasclient test")

esp.set_pin_mode(13, Direction.OUTPUT)

def blinkie(sleep_time = 0.1):
    esp.set_debug_level(False)
    for i in range(0, 10):
        esp.set_digital_write(13, 1)
        time.sleep(sleep_time)
        esp.set_digital_write(13, 0)
        time.sleep(sleep_time)
    esp.set_debug_level(3)

blinkie()
print("STATUS ", esp.status)
blinkie()
print("TEMP ", esp.temperature)
blinkie()
print("FIRMWARE ", esp.firmware_version)
blinkie()
print("STATUS ", esp.status)
blinkie()
print("FIRMWARE ", esp.firmware_version)
blinkie()
print("MAC ", esp.MAC_address)
blinkie()