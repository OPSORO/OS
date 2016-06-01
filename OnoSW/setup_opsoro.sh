#!/bin/sh

FOLDER=OnoSW/
SERVICE=opsoro
STARTFILE=__init__.py

# Copy script to init for daemon
sudo cp $SERVICE /etc/init.d/$SERVICE
# Add service to startup
sudo update-rc.d $SERVICE defaults
sleep .5

# Make sure we can run the script
sudo chmod +x $FOLDER$STARTFILE
sudo chmod 755 $FOLDER$STARTFILE

# Start service
sudo service $SERVICE start
sleep .5
# Check service status
sudo service $SERVICE status