import pyvisa
import time


rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())

r = rm.open_resource('TCPIP::sds1052.home::INSTR')
print("sds1052:",r.query('*IDN?'))
# print("set ASET")
# r.write('ASET')
# time.sleep(5)
#  See https://github.com/lxi-tools/lxi-tools/wiki/Siglent-SDS1000CML-CNL-series 
print("PKPK",r.query('C1:PAVA? ALL'))
print("RMS",r.query('C1:PAVA? RMS'))
print("FREQ",r.query('C1:PAVA? FREQ'))