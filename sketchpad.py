import pyvisa
import time
xpm1241=None


rm = pyvisa.ResourceManager('@py')
for x in range(10):
    print(x)
    # Look for Resources on USB
    xpm1241=None
    for resource in rm.list_resources('^ASRL/dev/ttyUSB'):
        rName  = resource
        try:
            r= rm.open_resource(rName,baud_rate=115200)
            if "XDM1241" in r.query('*IDN?'):
                print("resource:",resource)
                xpm1241 = r
        except:
            pass
    if xpm1241 != None:
        print(xpm1241.query('MEAS1:SHOW?'))

    time.sleep(5)






# owon1241 = rm.open_resource('ASRL/dev/ttyUSB0::INSTR',baud_rate=115200)
# print(owon1241.query('*IDN?'))
# for x in range(10):
#     print(owon1241.query('MEAS1:SHOW?'))
#     time.sleep(1)