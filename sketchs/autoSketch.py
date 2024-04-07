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
jds6600.configure(freq,5,0)
time.sleep(3)
sds1052 = Sds1052(quiet=True)
if not sds1052.connect():
    print("Error: Siglent sds1052 oscilloscope did not connect, ending....")
    exit(0)
time.sleep(3)
#  Main automation loop
while (start + 2000) > time.time():
    helper.writeStatus("auto","running",step,"")
    rowJson=helper.startRow(step)
    rowJson=helper.addRowMeasurement(rowJson,"frequency","",freq)

    #  Collect Measurements
    measure=sds1052.measure("PKPK")
    rowJson=helper.addRowMeasurement(rowJson,"sds1052","PKPK",str(measure["measure"]))
    measure=sds1052.measure("RMS")
    rowJson=helper.addRowMeasurement(rowJson,"sds1052","RMS",str(measure["measure"]))
    print("rowJson:",rowJson)
    tableJson=helper.addTableRow(tableJson,rowJson)

    #  Update JDS6600 frequency
    freq *= 1.059
    freq = round(freq, 1)
    if freq>20000:
        break
    jds6600.configure(freq,5,0)
    time.sleep(1)
    step+=1

#  Write the results
helper.writeJsonTable("auto",tableJson)