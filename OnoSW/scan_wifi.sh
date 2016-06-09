#!/bin/sh
truncate -s 0 /home/pi/OnoSW/apps/opsoroassistant/static/wifi
sudo python /home/pi/OnoSW/apps/WiFi/wifilist.py > /home/pi/OnoSW/apps/WiFi/static/wifi