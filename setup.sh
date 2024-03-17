#!/usr/bin/env bash

# Before running this file do the following on the raspbery pi
# Add git and your git info
# sudo apt -y install git
# git config --global user.name "scpipi"
# git config --global user.email ""
# git clone https://github.com/somervda/scpipi.git
# This file will now be in the pimidi folder


# Make sure apt is updated and we have the latest package lists before we start
# Remember to 'chmod u+x setup.sh' to be able to run this script 
# then 'bash setup.sh'

date
echo 1. Updating and Upgrade apt packages 
sudo apt update -y
sudo apt upgrade -y

echo 2. Installing and rationalizing Python Version Names
sudo apt install -y python-is-python3
sudo apt install -y python3-pip
sudo apt install -y python-dev-is-python3

python --version
pip --version


echo 3. Installing OPi.GPIO 
# Install GPIO support for the orange PI 
# see https://pypi.org/project/RPi.GPIO/ and https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/ 
# Note: Use GPIO.setmode(GPIO.SUNXI) to use "PA01" style channel naming
pip install RPi.GPIO


echo 4. Installing python i2c and oled support
sudo usermod -a -G gpio pi

echo 5. Installing pyvisa instrument interface library
pip install -U pyvisa
pip install -U pyvisa-py

PATH=$PATH:/home/pi/.local/bin

echo 6. Install fastapi for web services and a ASGI web server
pip install fastapi
pip install "uvicorn[standard]"
# Note: I run uvicorn using this command during development
# uvicorn web:app --reload --host pimidi.home



# Add uvicorn.service to the /lib/systemd/system/ folder
# By default service is not enabled and stopped
echo 7. Setup the pimidi_uvicorn.service to run on startup 
sudo cp uvicorn.service /lib/systemd/system/uvicorn.service
# sudo systemctl enable uvicorn.service
# sudo systemctl start uvicorn.service 
sudo systemctl status uvicorn.service 

date