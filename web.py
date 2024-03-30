#!/usr/bin/python3

# The main entrypoint for the scpipi application
# Runs in a fastAPI server to accept web service calls
# Note for testing 
# uvicorn web:app --reload --host scpipi.local

import sys
import time
import asyncio
# import pyvisa



# fastAPI 
from typing import Union,Annotated
from fastapi import FastAPI,Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from xdm1241 import Xdm1241
from jds6600 import Jds6600


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# *** Owon xdm1241 multimedia web services ********

xdm1241 = Xdm1241(quiet=True)

@app.get("/xdm1241/connect")
def xdm1241Connect():
    return xdm1241.connect()

@app.get("/xdm1241/config/{type}/{range}/{rate}")
def xdm1241Config(type: Annotated[str, Path(title="type: voltdc,voltac,currdc,currac,res,temp")],
    range: Annotated[int, Path(title="range: auto=0  or 1-9 for specific range (see programming manual)")], 
    rate: Annotated[int, Path(title="rate: (0=Slow, 1=Medium 2=Fast)")]):
    return xdm1241.configure(type,range,rate)


@app.get("/xdm1241/measureShow")
def xdm1241measure(): 
    return xdm1241.measureShow()

@app.get("/xdm1241/measure")
def xdm1241measure(): 
    return xdm1241.measure()

@app.get("/xdm1241/type")
def xdm1241type(): 
    return xdm1241.type

@app.get("/xdm1241/range")
def xdm1241range(): 
    return xdm1241.range

@app.get("/xdm1241/rate")
def xdm1241rate(): 
    return xdm1241.rate

@app.get("/xdm1241/isConnected")
def xdm1241isConnected(): 
    return xdm1241.isConnected()

# *** jds6600 signal generator web services

jds6600 = Jds6600(quiet=True)

@app.get("/jds6600/connect")
def jds6600Connect():
    return jds6600.connect()

@app.get("/jds6600/isConnected")
def jds6600isConnected(): 
    return jds6600.isConnected()

@app.get("/jds6600/config/{freq}/{level}/{wave}")
def xdm1241Config(freq: Annotated[float, Path(title="frequency in Hz , max 30MHz")],
    level: Annotated[float, Path(title="Output level in volts")], 
    wave: Annotated[int, Path(title="waveform (0=sine,1=square etc)")]):
    return jds6600.configure(freq,level,wave)

# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
app.mount("/", StaticFiles(directory="static", html=True), name="static")