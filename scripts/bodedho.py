#!/usr/bin/python3

import sys
sys.path.append("lib")

from xdm1241 import Xdm1241
from jds6600 import Jds6600
from sds1052 import Sds1052
from dho804 import Dho804
import time
import json
from helper import Helper

#  Setup environment
helper = Helper(quiet=True)
result=[]
start=time.time()
step=1
tableJson=""
jds6600 = Jds6600(quiet=True)
if not jds6600.connect():
    print("Error: jds6600 signal generator did not connect, ending....")
    exit(0)
freq=8
jds6600.configure(freq,1,0)
time.sleep(2)
dho804 = Dho804(quiet=True)
if not dho804.connect():
    print("Error: Rigol dho804 oscilloscope did not connect, ending....")
    exit(0)

#  Main automation loop
while (start + 300) > time.time():
    rowJson=helper.startRow(step)
    rowJson=helper.addRowMeasurement(rowJson,"frequency","",freq)
    helper.writeStatus("bodedho","running",step,"",freq)

    #  Collect Measurements
    measure=dho804.measure("VPP")
    rowJson=helper.addRowMeasurement(rowJson,"dho804","VPP",str(measure["measure"]))
    measure=dho804.measure("FREQ")
    rowJson=helper.addRowMeasurement(rowJson,"dho804","FREQ",str(measure["measure"]))
    print("rowJson:",rowJson)
    tableJson=helper.addTableRow(tableJson,rowJson)

    #  Update JDS6600 frequency
    freq *= 1.059
    if freq>20000:
        break
    freq = round(freq, 1)
    jds6600.configure(freq,1,0)
    time.sleep(1)
    step+=1

#  Write the results
helper.writeJsonTable("bodedho",tableJson)
helper.removeStatus()
