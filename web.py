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
# print(rm.list_resources())

# owon xpm1241 services

xpm1241 = rm.open_resource('ASRL/dev/ttyUSB0::INSTR',baud_rate=115200)

@app.get("/xpm1241/config/{type}/{rate}/{range}")
# type: voltdc,voltac,currdc,currac,res,temp
# rate: S/M/F (Slow/Medium/Fast sampling)
# range: auto,1-9
async def xpm1241Config(type: Annotated[str, Path(title="type: voltdc,voltac,currdc,currac,res,temp")],
    rate: Annotated[str, Path(title="rate: S/M/F (Slow/Medium/Fast sampling)")],
    range: Annotated[str, Path(title="range: auto,1-9")]): 
    # Build configuration string
    config = "CONFigure:"
    match type:
        case "voltdc" :
            config += "VOLT:DC"
        case "voltac" :
            config += "VOLT:AC"
        case "currdc" :
            config += "CURR:DC"
        case "currac" :
            config += "CURR:AC"
        case "res" :
            config += "RES"
        case "temp" :
            config += "TEMP"
    result= xpm1241.query(config)
    return{result}

# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
app.mount("/", StaticFiles(directory="static", html=True), name="static")