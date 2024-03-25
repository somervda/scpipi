#!/usr/bin/python3

import time
import pyvisa
import math

class Xdm1241:
    # owon _xdm1241 services
    #  See https://files.owon.com.cn/software/Application/XDM1000_Digital_Multimeter_Programming_Manual.pdf 
    # for scpi commands
    _type = ''
    _xdm1241 = None
    _range = ''
    _rate = ''
    _quiet = True

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self.rm = pyvisa.ResourceManager('@py')

    def connect(self):
        not self._quiet and print("connect")
        # Look for the _xdm1241 device among the resources
        self._xdm1241=None
        not self._quiet and  print(self.rm.list_resources())
        for resource in self.rm.list_resources('^ASRL/dev/ttyUSB'):
            name  = resource
            not self._quiet and print("Resource name:",name)
            try:
                resourceRef= self.rm.open_resource(name,baud_rate=115200)
                resourceId = resourceRef.query('*IDN?')
                not self._quiet and print("ResourseRef:",resourceRef," ResourceId:",resourceId)
                if "XDM1241" in resourceId:
                    self._xdm1241 = resourceRef
                    # Set to default configuration
                    time.sleep(.5)
                    self.congigure("voltdc",0,0)
                    break
            except Exception as inst:
                not self._quiet and print(inst)
                pass
        return  self.isConnected()

    def configure(self,type, range,rate):
        not self._quiet and print("configure",type,range,rate)
        self._type = ''
        self._range = ''
        self._rate = ''
        if not self.isConnected():
            not self._quiet and print("Connect to _xdm1241")
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
            not self._quiet and print("configCmd:",configCmd)
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
                not self._quiet and print("_xdm1241 oserror")
                self._xdm1241=None
                return False
        else:
            not self._quiet and print("No _xdm1241 found")
            return False


    def measure(self): 
        not self._quiet and print("measure")
        if not self.isConnected():
            not self._quiet and  print("Connect to _xdm1241")
            self.connect()
        if self.isConnected():
            try:
                result = self._xdm1241.query('MEAS1?')
                # Strip cr and lf from return value
                value = result.replace('\r','').replace('\n','')
                self.getPanelMeasure(value)
                return{value}
            except OSError:
                not self._quiet and print("_xdm1241 oserror")
                self._xdm1241 = None
                return{False}
        else:
            not self._quiet and print("No _xdm1241 found")
            return(False)

    def isConnected(self):
        not self._quiet and print("isConnected")
        if self._xdm1241:
            return True
        else: 
            return False
    
    def getPanelMeasure(self,measure):
        # Convert an scientific notation based value
        # into something to display on the led panel
        value = measure.split('E')
        mantisa = float(value[0])
        exp = int(value[1])
        print(mantisa,exp)
        # Work out scaling to show on pannel i.e. micro, milli, killo, mega
        scale = ""
        if exp< -6:
            scale = "micro"
            expAdj = exp - -6
            disp = mantisa * (10**expAdj)
        elif exp< -3:
            scale = "milli"
            expAdj = exp - -3
            disp = mantisa * (10**expAdj)
        elif exp>= 6:
            scale = "mega"
            expAdj = exp - 6
            disp = mantisa * (10**expAdj)
        elif exp>= 3:
            scale = "killo"
            expAdj = exp - 3
            disp = mantisa * (10**expAdj)
        else:
            scale = ""
            expAdj = exp 
            disp = mantisa * (10**expAdj)    
        print(scale,disp)  
        pass

    # Getters

    def get_type(self):
        not self._quiet and print("get_type")
        return self._type
    type = property(get_type)

    def get_range(self):
        not self._quiet and print("get_range")
        return self._range
    range = property(get_range)

    def get_rate(self):
        not self._quiet and print("get_rate")
        return self._rate
    rate = property(get_rate)