#!/usr/bin/python3

import time
import pyvisa

rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())



# owon xpm1241 services
#  See https://files.owon.com.cn/software/Application/XDM1000_Digital_Multimeter_Programming_Manual.pdf 
# for scpi commands
xpm1241 = None



@app.get("/xpm1241/connect")
def xpm1241Connect():
    global xpm1241
    # Look for the xpm1241 device among the resources
    xpm1241=None
    for resource in rm.list_resources('^ASRL/dev/ttyUSB'):
        name  = resource
        try:
            r= rm.open_resource(name,baud_rate=115200)
            if "XDM1241" in r.query('*IDN?'):
                print("r:",r,"name:",name)
                xpm1241 = r
        except:
            pass
    if xpm1241:
        return True
    else:
        return False

@app.get("/xpm1241/config/{type}/{range}/{rate}")
async def xpm1241Config(type: Annotated[str, Path(title="type: voltdc,voltac,currdc,currac,res,temp")],
    range: Annotated[int, Path(title="range: auto=0  or 1-9 for specific range (see programming manual)")], 
    rate: Annotated[int, Path(title="rate: (0=Slow, 1=Medium 2=Fast)")]):
    global xpm1241
    if not xpm1241:
        # print("Connect to xpm1241")
        xpm1241Connect()
    if xpm1241:
        # Build configCmduration string
        configCmd = "CONFigure:"
        if type== "voltdc" :
            configCmd += "VOLT:DC"
            if range == 1:
                configCmd += " 500E-3"
            elif range == 2:
                configCmd += " 5"
            elif range == 3:
                configCmd += " 50"
            elif range == 4:
                configCmd += " 500"
            elif range == 5:
                configCmd += " 1000"
            else:
                configCmd += " AUTO"
        elif type ==  "voltac" :
            configCmd += "VOLT:AC"
            if range == 1:
                configCmd += " 500E-3"
            elif range == 2:
                configCmd += " 5"
            elif range == 3:
                configCmd += " 50"
            elif range == 4:
                configCmd += " 500"
            elif range == 5:
                configCmd += " 750"
            else:
                configCmd += ":AUTO"
        elif type ==  "currdc" :
            configCmd += "CURR:DC"
            if range == 1:
                configCmd += " 5E-3"
            elif range == 2:
                configCmd += " 50E-3"
            elif range == 3:
                configCmd += " 500E-3"
            elif range == 4:
                configCmd += " 5"
            elif range == 5:
                configCmd += " 10"
            else:
                configCmd += " AUTO"
        elif type ==   "currac" :
            configCmd += "CURR:AC"
            if range == 1:
                configCmd += " 5E-3"
            elif range == 2:
                configCmd += " 50E-3"
            elif range == 3:
                configCmd += " 500E-3"
            elif range == 4:
                configCmd += " 5"
            elif range == 5:
                configCmd += " 10"
            else:
                configCmd += " AUTO"
        elif type ==   "res" :
            configCmd += "RES"
            if range == 1:
                configCmd += " 500"
            elif range == 2:
                configCmd += " 5E3"
            elif range == 3:
                configCmd += " 50E3"
            elif range == 4:
                configCmd += " 500E3"
            elif range == 5:
                configCmd += " 5E6"
            elif range == 6:
                configCmd += " 50E6"
            else:
                configCmd += " AUTO"
        elif type ==  "freq" :
            configCmd += "FREQ"
        elif type ==  "temp" :
            configCmd += "TEMP"
        print(configCmd)
        # Also build the rate command
        rateCmd = "RATE "
        if rate== 1 :
            rateCmd += "M"
        elif rate == 2 :
            rateCmd += "F"
        else:
            rateCmd += "S"

        try:
            # Set rate,type and range
            result= xpm1241.write(rateCmd)
            time.sleep(.1)
            result= xpm1241.write(configCmd)
            time.sleep(.1)
            try:
                # Check we are really connected 
                # by doing a dummy query
                testResult = xpm1241.query('MEAS1?')
            except:
                xpm1241 = None
                return False
            else:
                return True
        except OSError:
            # print("xpm1241 oserror")
            xpm1241 = None
            return False
    else:
        print("No xpm1241 found")
        return False


@app.get("/xpm1241/measure")
async def xpm1241configCmd(): 
    global xpm1241
    if not xpm1241:
        # print("Connect to xpm1241")
        xpm1241Connect()
    if xpm1241:
        try:
            result = xpm1241.query('MEAS1?')
            return{result}
        except OSError:
            # print("xpm1241 oserror")
            xpm1241 = None
            return{False}
    else:
        # print("No xpm1241 found")
        return(False)