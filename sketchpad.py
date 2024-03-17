import pyvisa
import time
rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())
owon1241 = rm.open_resource('ASRL/dev/ttyUSB0::INSTR',baud_rate=115200)
print(owon1241.query('*IDN?'))
for x in range(10):
    print(owon1241.query('MEAS1:SHOW?'))
    time.sleep(1)