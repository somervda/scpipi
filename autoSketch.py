#!/usr/bin/python3

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
jds6600 = Jds6600(quiet=True)
if not jds6600.connect():
    print("Error: jds6600 signal generator did not connect, ending....")
    exit(0)
freq=8
sds1052 = Sds1052(quiet=True)
if not sds1052.connect():
    print("Error: Siglent sds1052 oscilloscope did not connect, ending....")
    exit(0)

#  Main automation loop
while (start + 500) > time.time():
    stepJson=helper.makeStepJson(step)
    jds6600.configure(freq,5,0)
    time.sleep(1)

    #  Collect Measurements
    measure=sds1052.measure("PKPK")
    stepJson=helper.addStepJson(stepJson,"sds1052","PKPK",str(measure["measure"]))
    measure=sds1052.measure("FREQ")
    if measure["success"]:
        stepJson=helper.addStepJson(stepJson,"sds1052","FREQ",str(measure["measure"]))
    print("{" + stepJson + "},")

    #  Update JDS6600 frequency
    freq *= 1.059
    if freq>10000:
        break
    time.sleep(2)
    step+=1