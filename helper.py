#!/usr/bin/python3
import datetime


class Helper:
    _quiet = True

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")

    def addStepJson(self,stepJson,deviceName,type,measure): 
        # Format a measurement into a json string and add it to
        # any existing stepJson string
        not self._quiet and print("addStepJson")
        if stepJson != "":
            stepJson+=","
        stepJson += '"' + deviceName + "-" + type + '":' + str(measure) 
        return stepJson

    def makeStepJson(self,step): 
        not self._quiet and print("makeStepJson")
        now = datetime.datetime.now()
        iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 
        stepJson = '"step":' + str(step) + ',"timestamp":"' + iso_time + '"' 
        return stepJson