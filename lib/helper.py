#!/usr/bin/python3
import datetime
import time
import json
import glob
import os
import signal
import psutil


class Helper:
    _quiet = True
    name = ""
    

    def __init__(self,name,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self.lastTime= time.time()
        self.name = name

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
        iso_time = now.strftime("%Y-%m-%dT%H:%M:%S") 
        rowJson = '"step":' + str(step) + ',"timestamp":"' + iso_time + '"' 
        return rowJson
    
    def addTableRow(self,tableJson,rowJson): 
        # Add a json row to the automation output table
        if tableJson == "" :
            tableJson += "{" + rowJson + "}\r\n"
        else:
            tableJson += ",{" + rowJson + "}\r\n"
        # Write latest verion of table every minute
        if (time.time()> self.lastTime + 60):
            self.writeJsonTable(tableJson)
            self.lastTime = time.time()
        return tableJson

    def writeJsonTable(self,tableJson):
        with open("results/" + self.name + ".json", "w") as result_file:
            result_file.write("[" + tableJson + "]")

    def writeStatus(self,state,step,message,freq=-1):
        # Check if there is a kill.now file in which case
        # clean things up and exit the script
        if os.path.isfile("./scripts/kill.now"):
            self.removeStatus()
            try:
                os.remove("./scripts/kill.now")
            except:
                pass
            exit(0)


        with open("scripts/status.json", "w") as status_file:
            status = {}
            status["name"] = self.name
            status["state"] = state
            status["step"] = step
            if freq != -1 :
                status["freq"] = freq
            status["message"] = message
            status_file.write(json.dumps(status))

    def getStatus(self):
        status = {}
        # Check if there is a ststus.json file present
        try:
            with open("scripts/status.json","r") as status_file:
                status = json.load(status_file)
        except:
            pass
        # Check if there are any running scripts
        for process in psutil.process_iter():
            if len(process.cmdline())>=2:
                if "scripts/" in process.cmdline()[1]:
                    status["pid"] = process.pid
        return (status)

    def killScript(self):
        try:
            with open("scripts/kill.now", "w") as kill_file:
                kill_file.write("")
            return True
        except exception as e:
            print("killScript error:",e)
            return False


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
