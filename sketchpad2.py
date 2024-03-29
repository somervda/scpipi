import pyvisa
import time


rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())

def processMeasurement(measure):
    # Pull apart the returned measurement
    # Owons chinese encoding of degree and ohm symbols is
    # weird so some special processing of those
    mainText = ''
    subText = ''
    type = ''
    # Deal with special charactrers first
    if ord(measure[-1]) == 8451 :
        # Special case , ends with degrees centergrade
        type = "temp"
        mainText = measure[0:len(measure) - 1]
        subText = "\u00B0C"
    elif ord(measure[-1]) == 937 :
        # Deal with ohms symbol
        type = 'res'
        for n in range(0,(len(measure) -1 )):
            testChar = measure[n] 
            if not (testChar.isnumeric() or testChar =='.' or testChar =='-') :
                mainText = measure[0:n] 
                subText = measure[n:]
                break
    else:
        # Other measurements don't need any tricks to process
        if "VDC" in measure:
            type = "voltdc"
        elif "VAC" in measure:
            type = "voltac"
        elif "ADC" in measure:
            type = "currdc"
        elif "AAC" in measure:
            type = "currac"
        elif "Hz" in measure:
            type = "freq"
        elif "F" in measure:
            type = "cap"
        for n in range(0,(len(measure) -1 )):
            testChar = measure[n] 
            if not (testChar.isnumeric() or testChar =='.' or testChar =='-') :
                mainText = measure[0:n] 
                subText = measure[n:]
                break
    print(measure," type:",type," mainText:",mainText," subText:",subText)
    # print(measure[-1], " ",ord(measure[-1]))

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
    xpm1241.encoding="euc_cn"
    processMeasurement(xpm1241.query('MEAS1:SHOW?').replace('\r','').replace('\n',''))

