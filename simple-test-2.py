import board
import busio
from digitalio import DigitalInOut
from time import sleep
from adafruit_bus_device.i2c_device import I2CDevice

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
  msg = [0] * (len(ls) + 1)
  msg[0] = len(ls)
  ndx = 1
  for v in ls:
    msg[ndx] = v
    ndx += 1
  return msg

def write_msg(tag, ls, addr = 0x2A, stp = False):
  # print(tag + "\n")
  msg = make_msg(ls)
  # print("SENDING: ", bytes(msg))
  with device:
    device.write(bytes(msg))
  #i2c.writeto(addr, bytes(msg), stop = stp)

# 0x00 is INPUT
# 0x01 is OUTPUT
INPUT = const(0x00)
OUTPUT = const(0x01)
def pinMode(pin, mode):
  # 0xA0 is pinMode
  # 4 is pin number
  # 6 is pin mode
  #       0     1     2     3    4     5     6
  ls = [0xE0, 0x50, 0x00, 0x00, pin, 0x00, mode]
  write_msg("pinMode()", ls)
  #result = bytearray(READ_BUF_SIZE)
  #i2c.readfrom_into(ADDR, result)
  # print(result)

HIGH = const(0x01)
LOW  = const(0x00)
def digitalWrite(pin, lvl):
  # 0x51 digitalWrite
  # 4 is pin
  # 6 is level
  #       0     1     2     3   4     5     6
  ls = [0xE0, 0x51, 0x00, 0x00, pin, 0x00, lvl]
  write_msg("digitalWrite({0})".format(lvl), ls)
  #print("Reading response to digitalWrite")
  #result = bytearray(READ_BUF_SIZE)
  #i2c.readfrom_into(ADDR, result)
  #print(result)
  #sleep(2)


#print("Trying lock...")
#while not i2c.try_lock():
#  pass

# print("Scanning...")
#print(i2c.scan())
#sleep(0.5)

#pinMode(13, OUTPUT)
#while True:
#  digitalWrite(13, HIGH)
#  sleep(1)
#  digitalWrite(13, LOW)
#  sleep(1)

# i2c.unlock()


ls = [0xAD, 0xAF, 0x1, 0x1, 0x2A, 0xDA]

# write_msg("digitalWrite({0})".format(lvl), ls)
with device:
  device.write(bytes(ls))

sleep(2)

ls = [0xAD, 0xAF, 0x03, 0x02, 0x01, 0x01, 0xDE, 0xAD, 0xBE, 0xEF, 0xDA]
with device:
  device.write(bytes(ls))

sleep(2)

a = list(bytearray("testing"))
b = list(bytearray("one"))
c = list(bytearray("two"))

ls = [0xAD, 0xAF, 0x03, len(a), len(b), len(c)] + a + b + c + [0xAD]
print(ls)
with device:
  device.write(bytes(ls))

print("Done")