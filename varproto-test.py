import board
import busio
from digitalio import DigitalInOut
from time import sleep
from adafruit_bus_device.i2c_device import I2CDevice
import neopixel, random

pxl = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c = busio.I2C(board.SCL, board.SDA)
ADDR = 0x2A
device = I2CDevice(i2c, ADDR)

# pylint: disable=bad-whitespace
_SET_NET_CMD           = const(0x10)
_SET_PASSPHRASE_CMD    = const(0x11)
_SET_DEBUG_CMD         = const(0x1A)

_GET_CONN_STATUS_CMD   = const(0x20)
_GET_IPADDR_CMD        = const(0x21)
_GET_MACADDR_CMD       = const(0x22)
_GET_CURR_SSID_CMD     = const(0x23)
_GET_CURR_RSSI_CMD     = const(0x25)
_GET_CURR_ENCT_CMD     = const(0x26)

_SCAN_NETWORKS         = const(0x27)
_GET_SOCKET_CMD        = const(0x3F)
_GET_STATE_TCP_CMD     = const(0x29)
_DATA_SENT_TCP_CMD     = const(0x2A)
_AVAIL_DATA_TCP_CMD    = const(0x2B)
_GET_DATA_TCP_CMD      = const(0x2C)
_START_CLIENT_TCP_CMD  = const(0x2D)
_STOP_CLIENT_TCP_CMD   = const(0x2E)
_GET_CLIENT_STATE_TCP_CMD = const(0x2F)
_DISCONNECT_CMD        = const(0x30)
_GET_IDX_RSSI_CMD      = const(0x32)
_GET_IDX_ENCT_CMD      = const(0x33)
_REQ_HOST_BY_NAME_CMD  = const(0x34)
_GET_HOST_BY_NAME_CMD  = const(0x35)
_START_SCAN_NETWORKS   = const(0x36)
_GET_FW_VERSION_CMD    = const(0x37)
_PING_CMD              = const(0x3E)

_SEND_DATA_TCP_CMD     = const(0x44)
_GET_DATABUF_TCP_CMD   = const(0x45)
_SET_ENT_IDENT_CMD     = const(0x4A)
_SET_ENT_UNAME_CMD     = const(0x4B)
_SET_ENT_PASSWD_CMD    = const(0x4C)
_SET_ENT_ENABLE_CMD    = const(0x4F)

_SET_PIN_MODE_CMD      = const(0x50)
_SET_DIGITAL_WRITE_CMD = const(0x51)
_SET_ANALOG_WRITE_CMD  = const(0x52)

_START_CMD             = const(0xE0)
_END_CMD               = const(0xEE)
_ERR_CMD               = const(0xEF)
_REPLY_FLAG            = const(1<<7)
_CMD_FLAG              = const(0)

SOCKET_CLOSED      = const(0)
SOCKET_LISTEN      = const(1)
SOCKET_SYN_SENT    = const(2)
SOCKET_SYN_RCVD    = const(3)
SOCKET_ESTABLISHED = const(4)
SOCKET_FIN_WAIT_1  = const(5)
SOCKET_FIN_WAIT_2  = const(6)
SOCKET_CLOSE_WAIT  = const(7)
SOCKET_CLOSING     = const(8)
SOCKET_LAST_ACK    = const(9)
SOCKET_TIME_WAIT   = const(10)

WL_NO_SHIELD          = const(0xFF)
WL_NO_MODULE          = const(0xFF)
WL_IDLE_STATUS        = const(0)
WL_NO_SSID_AVAIL      = const(1)
WL_SCAN_COMPLETED     = const(2)
WL_CONNECTED          = const(3)
WL_CONNECT_FAILED     = const(4)
WL_CONNECTION_LOST    = const(5)
WL_DISCONNECTED       = const(6)
WL_AP_LISTENING       = const(7)
WL_AP_CONNECTED       = const(8)
WL_AP_FAILED          = const(9)
# pylint: enable=bad-whitespace

READ_BUF_SIZE = 32
msg = [0] * READ_BUF_SIZE

def make_msg(ls):
  msg[0] = 0xAD
  msg[1] = 0xAF
  msg[2] = len(ls)
  c1 = 0
  for subls in ls:
    msg[3 + c1] = len(subls)
    c1 = c1 + 1
  c2 = 0
  for subls in ls:
    for e in subls:
      msg[3 + c1 + c2] = e
      c2 = c2 + 1
  # NON CRC
  msg[3 + c1 + c2] = 255
  return (3 + c1 + c2)

def write_msg(tag, ls, addr = 0x2A, stp = False):
  # print(tag + "\n")
  end = make_msg(ls) + 1
  # print("SENDING: ", bytes(msg)[0:end])
  with device:
    device.write(bytes(msg), end = end)

# 0x00 is INPUT
# 0x01 is OUTPUT
INPUT = const(0x00)
OUTPUT = const(0x01)
def pinMode(pin, mode):
  ls = [[_SET_PIN_MODE_CMD], [pin], [mode]]
  write_msg("pinMode({0}, {1})".format(pin, mode), ls)

HIGH = const(0x01)
LOW  = const(0x00)
def digitalWrite(pin, lvl):
  ls = [[_SET_DIGITAL_WRITE_CMD], [pin], [lvl]]
  write_msg("digitalWrite({0}, {1})".format(pin, lvl), ls)


pxl[0] = (random.randint(60, 120), random.randint(60, 120), random.randint(60, 120))
pxl.show()

SLEEP_TIME = 0.01
pinMode(13, OUTPUT)
while True:
  digitalWrite(13, HIGH)
  sleep(SLEEP_TIME)
  digitalWrite(13, LOW)
  sleep(SLEEP_TIME)

print("Done")