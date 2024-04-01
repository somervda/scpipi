#!/usr/bin/python3

import time
import pyvisa
import math
import traceback

class Sds1052:
    # Sds1052 Oscilloscope services
    #  See https://siglentna.com/wp-content/uploads/dlm_uploads/2023/04/SDS-Series_ProgrammingGuide_EN11D.pdf
    # for scpi commands

    _sds1052 = None
    _quiet = True
    rm = None

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self.rm = pyvisa.ResourceManager('@py')
        not self._quiet and print(self.rm.list_resources())

    def connect(self):
        not self._quiet and print("connect")
        # Open the sds1052 device 
        # Its a tcpIP interface so connection to host either works or it doesnt
        try:
            resource=self.rm.open_resource('TCPIP::sds1052.home::INSTR')
            time.sleep(1)
            # Test by sending first channel on command
            resourceId = resource.query('*IDN?')
            not self._quiet and print(" ResourceId:",resourceId)
            if "SDS1052DL+" in resourceId:
                not self._quiet and print("sds1052 found:",resource)
                self._sds1052 = resource
        except Exception as inst:
            not self._quiet and print(inst)
        return self.isConnected()


    def isConnected(self):
        not self._quiet and print("isConnected")
        if self._sds1052:
            return True
        else: 
            return False

    def measure(self,type): 
        # Return requested measurement type from wave on channel 1 as a float
        # Typical measutement types are RMS,PKPK,FREQ,MIN,MAX,PHA
        # PHA is special , it uses the command below to get phase difference
        # between waves on channel and 2
        # MEAD PHA,C1-C2  (Phase between C1 and C2)
        not self._quiet and print("measure")
        if not self.isConnected():
            not self._quiet and  print("Connect to _sds1052")
            self.connect()
        if self.isConnected():
            try:
                measure=0
                if type=="PHA":
                    # May be a bit more to it than this....
                    measure = self._sds1052.query('C1-C2:MEAD? PHA').replace('\r','').replace('\n','')
                else:
                    measure = self._sds1052.query('C1:PAVA? ' + type).replace('\r','').replace('\n','')
                not self._quiet and print("measure:",measure)
                measureInfo = {}
                prefix = ""
                measureInfo["success"] = True
                measureInfo["measure"] = self.processMeasure(measure,type)
                measureInfo["type"] = type
                if measureInfo["measure"] < 0.001:
                    measureInfo["mainText"] = str(measureInfo["measure"] * 1000)[0:6]
                    prefix="milli-"
                else:
                    measureInfo["mainText"] = str(measureInfo["measure"])
                volts=["PKPK","MIN","MAX","AMPL","MEAN"]
                seconds=["RISE","FALL"]
                hertz=["FREQ"]
                degrees=["PHA"]
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
                not self._quiet and print("sds1052 measure error", e,traceback.format_exc())
                self._sds1052 = None
                measureInfo = {}
                measureInfo["success"] = False
                return measureInfo
        else:
            not self._quiet and print("No _sds1052 found")
            measureInfo = {}
            measureInfo["success"] = False
            return measureInfo

    def processMeasure(self,measure,type):
        not self._quiet and print("processMeasure",measure,type)
        # Pull out the actual measurement value as a float
        #  i.e. C1:PAVA RMS,1.76E+00V -> 1.76
        measureParts = measure.split(',')
        not self._quiet and print("measure:",measure, " measureParts:",measureParts)
        if len(measureParts)==2:
            # Process the second part of the measure
            measureCore = ""
            if type=="FREQ":
                measureCore = measureParts[1].replace('Hz','')
            elif type=="PHA":
                measureCore = measureParts[1].replace('degree','')
            else:
                measureCore = measureParts[1][:-1]
            not self._quiet and print("measureCore:",measureCore)
            return float(measureCore)
        else:
            return -1

