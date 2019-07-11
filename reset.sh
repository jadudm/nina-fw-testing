esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART erase_flash
esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash -z 0x1000 ../setup/esp32-20190615-v1.11-45-g14cf91f70.bin
