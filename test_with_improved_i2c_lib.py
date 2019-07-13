import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction

from time import sleep
import neopixel, random
from adafruit_esp32i2c import adafruit_esp32i2c

pxl = neopixel.NeoPixel(board.NEOPIXEL, 1)

# SCK is ...
# MOSI is ...
# MISO is ...
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32i2c.ESP_I2Ccontrol(None, None, None, None, debug = False)
esp.set_pin_mode(13, Direction.OUTPUT)
SLEEP_TIME = 0.1
while True:
  esp.set_digital_write(13, 1)
  sleep(SLEEP_TIME)
  esp.set_digital_write(13, 0)
  sleep(SLEEP_TIME)