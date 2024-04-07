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
        timer = time.time() + timeout
        while timer >  time.time() and not self.isConnected():
            not self._quiet and print("Connecting...")
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
            time.sleep(1)
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
            elif type ==   "cap" :
                configCmd += "CAP"
                if range == 1:
                    configCmd += " 50E-9"
                elif range == 2:
                    configCmd += " 500E-9"
                elif range == 3:
                    configCmd += " 5E-6"
                elif range == 4:
                    configCmd += " 50E-6"
                elif range == 5:
                    configCmd += " 500E-6"
                elif range == 6:
                    configCmd += " 5E-3"
                elif range == 7:
                    configCmd += " 50E-3"
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


    def measureShow(self):
        # Returns process version of measure
        # and supporting information 
        not self._quiet and print("measureShow")
        if not self.isConnected():
            not self._quiet and  print("Connect to _xdm1241")
            self.connect()
        if self.isConnected():
            try:
                self._xdm1241.encoding="euc_cn"
                measure = self._xdm1241.query('MEAS1:SHOW?').replace('\r','').replace('\n','')
                not self._quiet and print("measure:",measure)
                # Strip cr and lf from return value
                return self.processMeasurement(measure)
            except Exception as e:
                not self._quiet and print("_xdm1241 measure error", e)
                self._xdm1241 = None
                measureInfo = {}
                measureInfo["success"] = False
                return measureInfo
        else:
            not self._quiet and print("No _xdm1241 found")
            measureInfo = {}
            measureInfo["success"] = False
            return measureInfo

    def measure(self): 
        # Return measure as a float
        not self._quiet and print("measure")
        if not self.isConnected():
            not self._quiet and  print("Connect to _xdm1241")
            self.connect()
        if self.isConnected():
            try:
                measure = float(self._xdm1241.query('MEAS?').replace('\r','').replace('\n',''))
                not self._quiet and print("measure:",measure)
                measureInfo = {}
                measureInfo["success"] = True
                measureInfo["measure"] = measure
                return measureInfo
            except Exception as e:
                not self._quiet and print("_xdm1241 measure error", e)
                self._xdm1241 = None
                measureInfo = {}
                measureInfo["success"] = False
                return measureInfo
        else:
            not self._quiet and print("No _xdm1241 found")
            measureInfo = {}
            measureInfo["success"] = False
            return measureInfo

    def isConnected(self):
        not self._quiet and print("isConnected")
        if self._xdm1241:
            return True
        else: 
            return False
    
    def processMeasurement(self,measure):
        # Pull apart the returned measurement
        # Owons chinese encoding of degree and ohm symbols is
        # weird so some special processing of those
        mainText = ''
        subText = ''
        # Deal with special charactrers first
        if ord(measure[-1]) == 8451 :
            # Special case , ends with degrees centergrade
            self._type = "temp"
            mainText = measure[0:len(measure) - 1]
            subText = "\u00B0C"
        elif ord(measure[-1]) == 937 :
            # Deal with ohms symbol
            self._type = 'res'
            for n in range(0,(len(measure) -1 )):
                testChar = measure[n] 
                if not (testChar.isnumeric() or testChar =='.' or testChar =='-') :
                    mainText = measure[0:n] 
                    subText = measure[n:]
                    break
        else:
            # Other measurements don't need any tricks to process
            if "VDC" in measure:
                self._type = "voltdc"
            elif "VAC" in measure:
                self._type = "voltac"
            elif "ADC" in measure:
                self._type = "currdc"
            elif "AAC" in measure:
                self._type = "currac"
            elif "Hz" in measure:
                self._type = "freq"
            elif "F" in measure:
                self._type = "cap"
            for n in range(0,(len(measure) -1 )):
                testChar = measure[n] 
                if not (testChar.isnumeric() or testChar =='.' or testChar =='-') :
                    mainText = measure[0:n] 
                    subText = measure[n:]
                    break
        not self._quiet and print(measure," type:",self._type," mainText:",mainText," subText:",subText)
        measureInfo = {}
        measureInfo["success"] = True
        measureInfo["value"] = measure
        measureInfo["mainText"] = mainText
        measureInfo["subText"] = subText
        measureInfo["type"] = self._type
        measureInfo["range"] = self._range
        measureInfo["rate"] = self._rate
        not self._quiet and print("measureInfo:",measureInfo)
        return (measureInfo)

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