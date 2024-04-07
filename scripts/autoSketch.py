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
sds1052 = Sds1052(quiet=True)
if not sds1052.connect():
    print("Error: Siglent sds1052 oscilloscope did not connect, ending....")
    exit(0)

#  Main automation loop
while (start + 20) > time.time():
    rowJson=helper.startRow(step)
    helper.writeStatus("auto","running",step,"")

    #  Collect Measurements
    measure=sds1052.measure("PKPK")
    rowJson=helper.addRowMeasurement(rowJson,"sds1052","PKPK",str(measure["measure"]))
    print("rowJson:",rowJson)
    tableJson=helper.addTableRow(tableJson,rowJson)
    time.sleep(1)
    step+=1

#  Write the results
helper.writeJsonTable("auto",tableJson)
helper.removeStatus()