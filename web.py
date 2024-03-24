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

from xpm1241 import Xpm1241


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make a xpm1241 object
xpm1241 = Xpm1241()

@app.get("/xpm1241/connect")
def xpm1241Connect():
    return xpm1241.connect()

@app.get("/xpm1241/config/{type}/{range}/{rate}")
def xpm1241Config(type: Annotated[str, Path(title="type: voltdc,voltac,currdc,currac,res,temp")],
    range: Annotated[int, Path(title="range: auto=0  or 1-9 for specific range (see programming manual)")], 
    rate: Annotated[int, Path(title="rate: (0=Slow, 1=Medium 2=Fast)")]):
    return xpm1241.configure(type,range,rate)

@app.get("/xpm1241/measure")
async def xpm1241measure(): 
    return xpm1241.measure()


# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
app.mount("/", StaticFiles(directory="static", html=True), name="static")