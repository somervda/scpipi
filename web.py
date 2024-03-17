#!/usr/bin/python3

# The main entrypoint for the scpipi application
# Runs in a fastAPI server to accept web service calls
# Note for testing 
# uvicorn web:app --reload --host scpipi.local

import sys
import time
import asyncio
import pyvisa



# fastAPI 
from typing import Union,Annotated
from fastapi import FastAPI,Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())



# owon xpm1241 services
xpm1241 = None

@app.get("/xpm1241/connect")
def xpm1241Connect():
    global xpm1241
    # Look for the xpm1241 device among the resources
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
    if xpm1241:
        return(True)
    else:
        return(False)

@app.get("/xpm1241/config/{type}/{rate}/{range}")
# type: voltdc,voltac,currdc,currac,res,temp
# rate: S/M/F (Slow/Medium/Fast sampling)
# range: auto,1-9
async def xpm1241Config(type: Annotated[str, Path(title="type: voltdc,voltac,currdc,currac,res,temp")],
    rate: Annotated[str, Path(title="rate: S/M/F (Slow/Medium/Fast sampling)")],
    range: Annotated[str, Path(title="range: auto,1-9")]): 
    global xpm1241
    if not xpm1241:
        print("Connect to xpm1241")
        xpm1241Connect()
    if xpm1241:
        # Build configuration string
        config = "CONFigure:"
        if type== "voltdc" :
            config += "VOLT:DC"
        elif type ==  "voltac" :
            config += "VOLT:AC"
        elif type ==  "currdc" :
            config += "CURR:DC"
        elif type ==   "currac" :
            config += "CURR:AC"
        elif type ==   "res" :
            config += "RES"
        elif type ==  "temp" :
            config += "TEMP"
        try:
            result= xpm1241.write(config)
            return{True}
        except OSError:
            print("xpm1241 oserror")
            xpm1241 = None
            return{False}
    else:
        print("No xpm1241 found")
        return(False)


# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
app.mount("/", StaticFiles(directory="static", html=True), name="static")