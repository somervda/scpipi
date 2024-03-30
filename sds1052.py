#!/usr/bin/python3

import time
import pyvisa
import math

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

    def connect(self):
        not self._quiet and print("connect")
        # Open the sds1052 device 
        # Its a tcpIP interface so connection to host either works or it doesnt
        resource=rm.open_resource('TCPIP::sds1052.home::INSTR')
        try:

            # Test by sending first channel on command
            resourceId = self._sds1052.query('*IDN?')
            not self._quiet and print(" ResourceId:",resourceId)
            if "SDS1052DL+" in resourceId:
                not self._quiet and print("sds1052 found:",resource)
                self._sds1052 = resource
                break
        except Exception as inst:
            not self._quiet and print(inst)
        return isConnected()


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
                    measure = float(self._sds1052.query(r.query('MEAD PHA,C1-C2? ').replace('\r','').replace('\n',''))
                else:
                    measure = float(self._sds1052.query(r.query('C1:PAVA? ' + type).replace('\r','').replace('\n',''))
                not self._quiet and print("measure:",measure)
                measureInfo = {}
                measureInfo["success"] = True
                measureInfo["measure"] = measure
                return measureInfo
            except Exception as e:
                not self._quiet and print("_sds1052 measure error", e)
                self._sds1052 = None
                measureInfo = {}
                measureInfo["success"] = False
                return measureInfo
        else:
            not self._quiet and print("No _sds1052 found")
            measureInfo = {}
            measureInfo["success"] = False
            return measureInfo
