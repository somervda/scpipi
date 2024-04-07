import sys
sys.path.append("lib")

import pyvisa
import time


rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())

r = rm.open_resource('TCPIP::dso804.home::INSTR')
print("dho804:",r.query('*IDN?'))
# https://int.rigol.com/Public/Uploads/uploadfile/files/ftp/DS/%E6%89%8B%E5%86%8C/DS1000Z/EN/DS1000Z_ProgrammingGuide_EN.pdf
#  https://github.com/lxi-tools/lxi-tools/wiki/Rigol-DS1000Z-series
print("PKPK",r.query(':MEASure:ITEM? VRMS,CHANnel1'))

r.write(':MEASure:SETup:DSA CHANnel1')
r.write(':MEASure:SETup:DSB CHANnel2')
print(r.query(':MEASure:RPHase?' ))