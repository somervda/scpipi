#!/usr/bin/python3
import datetime
import json
import glob
import os


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
        with open("results/" + name + ".json", "w") as result_file:
            result_file.write("[" + tableJson + "]")

    def writeStatus(self,name,state,step,message,freq=-1):
        with open("scripts/status.json", "w") as status_file:
            status = {}
            status["name"] = name
            status["state"] = state
            status["step"] = step
            if freq != -1 :
                status["freq"] = freq
            status["message"] = message
            status_file.write(json.dumps(status))

    def getStatus():
        with open("scripts/status.json","r") as status_file:
            return (json.load(status_file))


    def removeStatus(self):
        try:
            os.remove("./scripts/status.json")
            return True
        except:
            return False


    def writeScript(self,name,script):
        try:
            with open("scripts/" + name + ".py", "w") as script_file:
                script_file.write(script)
            return True
        except exception as e:
            print("writeScript error:",e)
            return False

    def deleteScript(self,name):
        try:
            os.remove("scripts/" + name + ".py")
            return True
        except:
            return False


    def getScripts(self):
        return glob.glob("scripts/*.py")

    def getResults(self):
        return glob.glob("results/*.json")

    def getResult(self,name):
        with open("results/" + name + ".json","r") as results_file:
            return (json.load(results_file))

    def deleteResult(self,name):
        try:
            os.remove("results/" + name + ".json")
            return True
        except:
            return False

    def getSchemas(self):
        return glob.glob("schemas/*.json")

    def getSchema(self,name):
        with open("schemas/" + name + ".json","r") as schema_file:
            return (json.load(schema_file))
    
    def writeSchema(self,name,schema):
        # schema is structured (not string)
        try:
            with open("schemas/" + name + ".json","w") as schema_file:
                schema_file.write(json.dumps(schema))
            return True
        except exception as e:
            print("writeSchema error:",e)
            return False


    def deleteSchema(self,name):
        try:
            os.remove("schemas/" + name + ".json")
            return True
        except:
            return False
