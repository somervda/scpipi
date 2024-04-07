import sys
sys.path.append("lib")

import pyvisa
import time


rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())


# Look for Resources on USB
xpm1241=None
for resource in rm.list_resources('^ASRL/dev/ttyUSB'):
    rName  = resource
    try:
        r= rm.open_resource(rName,baud_rate=115200)
        if "XDM1241" in r.query('*IDN?'):
            print("XDM1241 found:",resource)
            xpm1241 = r
            break
    except:
        print("XDM1241 not found:")
if xpm1241 != None:
    x = float(xpm1241.query('MEAS?').replace('\r','').replace('\n',''))
    print(x)

