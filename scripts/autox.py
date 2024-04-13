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

#  Main automation loop
while (start + 110) > time.time():
    rowJson=helper.startRow(step)
    helper.writeStatus("auto","running",step,"")

    #  Collect Measurements
    print("rowJson:",rowJson)
    tableJson=helper.addTableRow(tableJson,rowJson)
    time.sleep(01)
    step+=1

#  Write the results
helper.writeJsonTable("auto",tableJson)
helper.removeStatus()
