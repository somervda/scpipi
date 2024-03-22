import pyvisa
import time


xpm1241=None


rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())




# Look for Resources on USB
jds6600=None
for resource in rm.list_resources('^ASRL/dev/ttyUSB'):
    rName  = resource
    try:
        r= rm.open_resource(rName,baud_rate=115200)
        # Test by sending first channel on command
        result=r.query(":w20=1,0.")
        print("Result:",result)
        if "ok" in result:
            print("jds6600 found:",resource)
            jds6600 = r
            break
    except:
        print("jds6600 not found:")
        pass

if jds6600 != None:
    #  Example talking to JDS6600 signal generator
    # See file://snas/Documents/Manuals/JT-JDS6600-Communication-protocol.pdf 
    # :<Action><Command>=<value>.
    # Action: i.e. w = write a command
    # Command: 20=channel select , 21=channel 1 waveform select, 22=channel 2 waveform select
    #          23=Channel 1 frequency set (In hundreth of a hertz), 24 = channel 2 frequency select  (In hundreth of a hertz)
    #          25 = Channel 1 range/level select in mv, 26 = Channel 2 range/level select in mv

    # Set only channel 1 on
    # Use this command to check we are connected to JDS6600
    result=jds6600.query(":w20=1,0.")
    print("Channel 1:",result)
    # If not :ok response then probably not JDS6600 device

    # set sine wave
    result=jds6600.query(":w21=0.")
    # Return OK if successful (And talking to the signal generator)
    print("Waveform 0:",result)

    result=jds6600.query(":w23=20000,0.")
    print("Frequency 200Hz",result)

    result=jds6600.query(":w25=1400.")
    print("Level 1.4V",result)


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
    print("xpm1241 reading:",xpm1241.query('MEAS1:SHOW?'))


# Siglent Oscilloscope
#  ASET (Auto setup to try and get good capture of waveform)
#  PACU PKPK, C1  (Page 86 get peak to peak reading)
#  See file://snas/Documents/Manuals/SDS1000-ProgrammingGuide_forSDS-1-1.pdf 

#     time.sleep(5)

r = rm.open_resource('TCPIP::sds1052.home::INSTR')
print(r.query('*IDN?'))
# print("set ASET")
# r.write('ASET')
# time.sleep(5)
#  See https://github.com/lxi-tools/lxi-tools/wiki/Siglent-SDS1000CML-CNL-series 
print("PKPK",r.query('C1:PAVA? ALL'))
print("RMS",r.query('C1:PAVA? RMS'))
print("FREQ",r.query('C1:PAVA? FREQ'))

# Test rigol
# https://int.rigol.com/Public/Uploads/uploadfile/files/ftp/DS/%E6%89%8B%E5%86%8C/DS1000Z/EN/DS1000Z_ProgrammingGuide_EN.pdf
#  https://github.com/lxi-tools/lxi-tools/wiki/Rigol-DS1000Z-series
r = rm.open_resource('TCPIP::DSO804.home::INSTR')
print(r.query('*IDN?'))
print("PKPK",r.query(':MEASure:ITEM? VRMS,CHANnel1'))







# owon1241 = rm.open_resource('ASRL/dev/ttyUSB0::INSTR',baud_rate=115200)
# print(owon1241.query('*IDN?'))
# for x in range(10):
#     print(owon1241.query('MEAS1:SHOW?'))
#     time.sleep(1)