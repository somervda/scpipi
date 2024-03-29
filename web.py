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


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make a xdm1241 object
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


# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
app.mount("/", StaticFiles(directory="static", html=True), name="static")