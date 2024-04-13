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
jds6600.configure(freq,2,0)
time.sleep(1)
sds1052 = Sds1052(quiet=True)
if not sds1052.connect():
    print("Error: Siglent sds1052 oscilloscope did not connect, ending....")
    exit(0)

#  Main automation loop
while (start + 3000) > time.time():
    rowJson=helper.startRow(step)
    rowJson=helper.addRowMeasurement(rowJson,"frequency","",freq)
    helper.writeStatus("auto","running",step,"",freq)

    #  Collect Measurements
    measure=sds1052.measure("PKPK")
    rowJson=helper.addRowMeasurement(rowJson,"sds1052","PKPK",str(measure["measure"]))
    print("rowJson:",rowJson)
    tableJson=helper.addTableRow(tableJson,rowJson)

    #  Update JDS6600 frequency
    freq *= 1.059
    if freq>200000:
        break
    freq = round(freq, 1)
    jds6600.configure(freq,2,0)
    time.sleep(1)
    step+=1

#  Write the results
helper.writeJsonTable("auto1004",tableJson)
helper.removeStatus()