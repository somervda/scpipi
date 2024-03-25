#!/usr/bin/python3

import time
import pyvisa
class Xdm1241:
    # owon _xdm1241 services
    #  See https://files.owon.com.cn/software/Application/XDM1000_Digital_Multimeter_Programming_Manual.pdf 
    # for scpi commands
    _type = ''
    _xdm1241 = None
    _range = ''
    _rate = ''

    def __init__(self):
        self.rm = pyvisa.ResourceManager('@py')

    def connect(self):
        # Look for the _xdm1241 device among the resources
        self._xdm1241=None
        print(self.rm.list_resources())
        for resource in self.rm.list_resources('^ASRL/dev/ttyUSB'):
            name  = resource
            print("Resource name:",name)
            try:
                resourceRef= self.rm.open_resource(name,baud_rate=115200)
                resourceId = resourceRef.query('*IDN?')
                print("ResourseRef:",resourceRef," ResourceId:",resourceId)
                if "XDM1241" in resourceId:
                    self._xdm1241 = resourceRef
                    break
            except Exception as inst:
                print(inst)
                pass
        return  self.isConnected()

    def configure(self,type, range,rate):
        self._type = ''
        self._range = ''
        self._rate = ''
        if not self.isConnected():
            print("Connect to _xdm1241")
            self.connect()
        if self.isConnected():
            # Build configCmduration string
            configCmd = "CONFigure:"
            if type== "voltdc" :
                configCmd += "VOLT:DC"
                if range == 1:
                    configCmd += " 500E-3"
                elif range == 2:
                    configCmd += " 5"
                elif range == 3:
                    configCmd += " 50"
                elif range == 4:
                    configCmd += " 500"
                elif range == 5:
                    configCmd += " 1000"
                else:
                    configCmd += " AUTO"
            elif type ==  "voltac" :
                configCmd += "VOLT:AC"
                if range == 1:
                    configCmd += " 500E-3"
                elif range == 2:
                    configCmd += " 5"
                elif range == 3:
                    configCmd += " 50"
                elif range == 4:
                    configCmd += " 500"
                elif range == 5:
                    configCmd += " 750"
                else:
                    configCmd += ":AUTO"
            elif type ==  "currdc" :
                configCmd += "CURR:DC"
                if range == 1:
                    configCmd += " 5E-3"
                elif range == 2:
                    configCmd += " 50E-3"
                elif range == 3:
                    configCmd += " 500E-3"
                elif range == 4:
                    configCmd += " 5"
                elif range == 5:
                    configCmd += " 10"
                else:
                    configCmd += " AUTO"
            elif type ==   "currac" :
                configCmd += "CURR:AC"
                if range == 1:
                    configCmd += " 5E-3"
                elif range == 2:
                    configCmd += " 50E-3"
                elif range == 3:
                    configCmd += " 500E-3"
                elif range == 4:
                    configCmd += " 5"
                elif range == 5:
                    configCmd += " 10"
                else:
                    configCmd += " AUTO"
            elif type ==   "res" :
                configCmd += "RES"
                if range == 1:
                    configCmd += " 500"
                elif range == 2:
                    configCmd += " 5E3"
                elif range == 3:
                    configCmd += " 50E3"
                elif range == 4:
                    configCmd += " 500E3"
                elif range == 5:
                    configCmd += " 5E6"
                elif range == 6:
                    configCmd += " 50E6"
                else:
                    configCmd += " AUTO"
            elif type ==  "freq" :
                configCmd += "FREQ"
            elif type ==  "temp" :
                configCmd += "TEMP"
            print(configCmd)
            # Also build the _rate command
            rateCmd = "RATE "
            if rate== 1 :
                rateCmd += "M"
            elif rate == 2 :
                rateCmd += "F"
            else:
                rateCmd += "S"

            try:
                # Set rate,type and range
                result= self._xdm1241.write(rateCmd)
                time.sleep(.1)
                result= self._xdm1241.write(configCmd)
                time.sleep(.1)
                try:
                    # Check we are really connected 
                    # by doing a dummy query
                    testResult = self._xdm1241.query('MEAS1?')
                except:
                    self._xdm1241=None
                    return False
                else:
                    self._type = type
                    self._range = range
                    self._rate = rate
                    return True
            except OSError:
                print("_xdm1241 oserror")
                self._xdm1241=None
                return False
        else:
            print("No _xdm1241 found")
            return False


    def measure(self): 
        if not self.isConnected():
            # print("Connect to _xdm1241")
            self.connect()
        if self.isConnected():
            try:
                result = self._xdm1241.query('MEAS1?')
                return{result}
            except OSError:
                print("_xdm1241 oserror")
                self._xdm1241 = None
                return{False}
        else:
            print("No _xdm1241 found")
            return(False)

    def isConnected(self):
        if self._xdm1241:
            return True
        else: 
            return False

    def get_type(self):
        return self._type

    type = property(get_type)

    def get_range(self):
        return self._range

    range = property(get_range)

    def get_rate(self):
        return self._rate

    rate = property(get_rate)