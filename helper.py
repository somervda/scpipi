#!/usr/bin/python3
import datetime


class Helper:
    _quiet = True

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")

    def addRowMeasurement(self,rowJson,deviceName,type,measure): 
        # Format a measurement into a json string and add it to
        # any existing rowJson string
        not self._quiet and print("addStepJson")
        if rowJson != "":
            rowJson+=","
        if type == "":
            rowJson += '"' + deviceName + '":' + str(measure) 
        else:
            rowJson += '"' + deviceName + "-" + type + '":' + str(measure) 
        return rowJson

    def startRow(self,step): 
        # Called at the start of a new automation output row
        # Adds the step number and a timestamp in iso format (Most standard available, works in excel)
        not self._quiet and print("makeStepJson")
        now = datetime.datetime.now()
        iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 
        rowJson = '"step":' + str(step) + ',"timestamp":"' + iso_time + '"' 
        return rowJson
    
    def addTableRow(self,tableJson,rowJson): 
        # Add a json row to the automation output table
        if tableJson == "" :
            tableJson += "{" + rowJson + "}\r\n"
        else:
            tableJson += ",{" + rowJson + "}\r\n"
        return tableJson

    def writeJsonTable(self,name,tableJson):
        with open("./results/" + name + ".json", "w") as result_file:
            result_file.write("[" + tableJson + "]")