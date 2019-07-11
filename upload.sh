#!/bin/bash 

# https://linuxize.com/post/bash-check-if-file-exists/
if [ -f "main.py" ]; then
  echo "main.py exists!"
  echo "Remove it, clean up, do what you have to..."
  echo "Then, try again."
  exit
fi

cp $1 main.py
echo "Uploading to ESP32 as main.py"
ampy -d 0.7 -p /dev/cu.SLAB_USBtoUART put main.py
echo "Removing main.py"
rm -f main.py

#echo "Resetting ESP32"
#ampy -d 0.7 -p /dev/cu.SLAB_USBtoUART reset
echo "Done"
