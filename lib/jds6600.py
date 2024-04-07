#!/usr/bin/python3

import time
import pyvisa
import math

class Jds6600:
    # jds6600 services
    #  See https://joy-it.net/files/files/Produkte/JT-JD6600/JT-JDS6600-Communication-protocol.pdf
    # for joyful commands

    _jds6600 = None
    _quiet = True
    _freq = 0
    _level = 0
    _wave = 0
    rm = None

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self.rm = pyvisa.ResourceManager('@py')

    def connect(self,timeout=5):
        not self._quiet and print("connect")
        # Look for the jds6600 device among the resources

        self._jds6600=None
        for resource in self.rm.list_resources('^ASRL/dev/ttyUSB'):
            rName  = resource
            timer = time.time() + timeout
            while timer >  time.time() and not self.isConnected():
                not self._quiet and print("Connecting...")
                try:
                    r= self.rm.open_resource(rName,baud_rate=115200)
                    # Test by sending first channel on command
                    result=r.query(":w20=1,0.")
                    not self._quiet and print("Result:",result)
                    if "ok" in result:
                        not self._quiet and print("jds6600 found:",resource)
                        self._jds6600 = r
                        break
                except Exception as inst:
                    not self._quiet and print(inst)
                timer.sleep(1)
        return  self.isConnected()

    def isConnected(self):
        not self._quiet and print("isConnected")
        if self._jds6600:
            return True
        else: 
            return False


    def configure(self,freq,level,wave):
        # Note: max frequence is 60Mhz
        not self._quiet and print("configure freq:",freq," level:",level," wave:",wave)
        self._freq = 0
        self._level = 0
        self._wave = 0
        if not self.isConnected():
            not self._quiet and print("Connect to jds6600")
            self.connect()
        if self.isConnected():
            try:
                # Set waveform on channel 1
                waveCmd = ":w21=" + str(wave) + "."
                result= self._jds6600.write(waveCmd)
                time.sleep(.1)
                # Set waveform on channel 1 (in HZ)
                freqCmd = ":w23=" + str(round(freq * 100,0)).replace('.0','') + ",0."  
                result= self._jds6600.write(freqCmd)
                time.sleep(.1)
                # Set level on channel 1 (in mV)
                levelCmd = ":w25=" + str(round(level * 1000,0)).replace('.0','') + "."  
                result= self._jds6600.write(levelCmd)
                time.sleep(.1)
                # Turn on channel 1
                result =  self._jds6600.write(":w20=1,0.")
                return True
            except Exception as e:
                not self._quiet and print(e)
                self._jds6600=None
                return False
        else:
            not self._quiet and print("No jds6600 found")
            return False            
