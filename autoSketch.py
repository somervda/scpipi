#!/usr/bin/python3

from xdm1241 import Xdm1241
from jds6600 import Jds6600
import time

#  Setup environment
freq = 8
xdm1241 = Xdm1241()
xdm1241.connect()
xdm1241.configure("voltac",0,0)

jds6600 = Jds6600()

# Run automation
while  freq <=20000:
    jds6600.configure(freq,3,0)
    print ("Freq:",freq," Measure:",xdm1241.measure())
    freq *= 1.0595
    time.sleep(1)
