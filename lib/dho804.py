#!/usr/bin/python3

import time
import pyvisa
import math
import traceback

class Dho804:
    # Dho804 Oscilloscope services
    # https://int.rigol.com/Public/Uploads/uploadfile/files/ftp/DS/%E6%89%8B%E5%86%8C/DS1000Z/EN/DS1000Z_ProgrammingGuide_EN.pdf
    #  https://github.com/lxi-tools/lxi-tools/wiki/Rigol-DS1000Z-series
    # for scpi commands

    _dho804 = None
    _quiet = True
    rm = None

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self.rm = pyvisa.ResourceManager('@py')
        not self._quiet and print(self.rm.list_resources())

    def connect(self,timeout=5):
        not self._quiet and print("connect")
        # Open the dho804 device 
        # Its a tcpIP interface so connection to host either works or it doesnt
        timer = time.time() + timeout
        while timer >  time.time() and not self.isConnected():
            not self._quiet and print("Connecting...")
            try:
                resource=self.rm.open_resource('TCPIP::dso804.home::INSTR')
                time.sleep(1)
                # Test by sending first channel on command
                resourceId = resource.query('*IDN?')
                not self._quiet and print(" ResourceId:",resourceId)
                if "DHO804" in resourceId:
                    not self._quiet and print("dho804 found:",resource)
                    self._dho804 = resource
                    # # Do an autoscale when connected
                    # print("autoscale")
                    # resource.write(':AUToscale')
                    # time.sleep(10)
                    break
            except Exception as inst:
                not self._quiet and print(inst)
            time.sleep(1)
        return self.isConnected()


    def isConnected(self):
        not self._quiet and print("isConnected")
        if self._dho804:
            return True
        else: 
            return False

    def fexp(self,f):
        return int(math.floor(math.log10(abs(f)))) if f != 0 else 0

    def fman(self,f):
        return f/10**self.fexp(f)

    def timebase(self,value):
        # Set the timebase to the value 
        # value must be in 1,2 or 5 steps 
        # and range from  5ns/div to 50s/div
        not self._quiet and print("timebase",value)
        if not self.isConnected():
            not self._quiet and  print("Connect to _dho804")
            self.connect()
        if self.isConnected():
            # try:
            if (value < 50 and value > 0.000000005):
                # round value to a step 
                exponent= self.fexp(value)
                mantisa= self.fman(value)
                if mantisa<2:
                    mantisa = 2
                elif mantisa<5:
                    mantisa=5
                else:
                    mantisa=1
                    exponent+=1
                scaleValue= mantisa * 10**exponent
                not self._quiet and print(':TIMebase:MAIN:SCALe ' + str(scaleValue))
                self._dho804.write(':TIMebase:MAIN:SCALe ' + str(scaleValue))
                return True
            else:
                return False

    def volts(self,value):
        # Set the volts per div to the value 
        # value must be in 1mv to 10V 
        not self._quiet and print("timebase",value)
        if not self.isConnected():
            not self._quiet and  print("Connect to _dho804")
            self.connect()
        if self.isConnected():
            # try:
            if (value <= 10 and value >= 0.001):
                self._dho804.write(':CHANnel1:SCALe ' + str(value))
                self._dho804.write(':CHANnel2:SCALe ' + str(value))
                return True
            else:
                return False

    def measure(self,type): 
        # Return requested measurement type from wave on channel 1 as a float
        # Typical measutement types are {VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|
        # VRMS|OVERshoot|PREShoot|MARea|MPARea|
        # PERiod|FREQuency|RTIMe|FTIMe|PWIDth|
        # NWIDth|PDUTy|NDUTy|RDELay|FDELay|
        # RPHase|FPHase|TVMAX|TVMIN|PSLEWrate|
        # NSLEWrate|VUPper|VMID|VLOWer|VARIance|
        # PVRMS|PPULses|NPULses|PEDGes|NEDGes}
        not self._quiet and print("measure",type)
        if not self.isConnected():
            not self._quiet and  print("Connect to _dho804")
            self.connect()
        if self.isConnected():
            try:
                measure=0
                if type in ["RPH","FPH"]:
                    # Phase measurements need 2 channels defined
                    print(':MEASure:ITEM? ' + type + ',CHANnel1,CHANnel2')
                    self._dho804.write(':MEASure:SETup:DSA CHANnel1')
                    self._dho804.write(':MEASure:SETup:DSB CHANnel2')
                    measure = self._dho804.query(':MEASure:' + type  + '?').replace('\r','').replace('\n','')
                else:
                    measure = self._dho804.query(':MEASure:ITEM? ' + type + ',CHANnel1').replace('\r','').replace('\n','')
                not self._quiet and print("measure:",measure)
                measureInfo = {}
                prefix = ""
                measureInfo["success"] = True
                measureInfo["measure"] = float(measure)
                measureInfo["type"] = type
                if abs(measureInfo["measure"]) < 0.001:
                    measureInfo["mainText"] = str(measureInfo["measure"] * 1000)[0:6]
                    prefix="milli-"
                else:
                    measureInfo["mainText"] = str(measureInfo["measure"])[0:6]
                volts=["VMAX","VMIN","VPP","VAMP","VAVG","VRMS"]
                seconds=["RTIM","FTIM"]
                hertz=["FREQ"]
                degrees=["RPH","FPH"]
                subText = ""
                if type in volts:
                    subText="Volts"
                elif type in seconds:
                    subText="Seconds"
                elif type in hertz:
                    subText="Hz"
                elif type in degrees:
                    subText="Degrees"
                measureInfo["subText"]=prefix + subText + " [" + type + "]"
                return measureInfo
            except Exception as e:
                not self._quiet and print("dho804 measure error", e,traceback.format_exc())
                self._dho804 = None
                measureInfo = {}
                measureInfo["success"] = False
                return measureInfo
        else:
            not self._quiet and print("No _dho804 found")
            measureInfo = {}
            measureInfo["success"] = False
            return measureInfo



