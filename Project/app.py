#!/usr/bin/env python3

from contextlib import asynccontextmanager
from datetime import datetime
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import pytz
from config.db import get_collection
from controllers.snmpcontroller import getsnmpdatacontroller, startup_event
logging.basicConfig(level=logging.INFO)
# Define the time zone for Bangkok
bangkok_tz = pytz.timezone('Asia/Bangkok')

# Load environment variables from .env file
pathenv = Path('./.env')
load_dotenv(dotenv_path=pathenv)

# Initialize the collection
collection = get_collection('snmp_data')

# Initialize FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Lifespan startup event triggered")
    # Startup task
    await startup_event()
    yield
    logging.info("Lifespan shutdown event triggered")
    # (Optional) Teardown task can be added here if needed

app = FastAPI(lifespan=lifespan)

# Collect data from the device
@app.get('/latest_snmp_data')
async def get_latest_snmp_data():
    latest_data = list(collection.find().sort([('time', -1)]).limit(100))
    return {"status": "success", "data": latest_data}

@app.get('/snmp_data')
def get_snmp_data():
    getsnmpdatacontroller()

@app.get('/snmp_data_range')
async def get_snmp_data_range(start_time: str, end_time: str):
    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    data = list(collection.find({
        'time': {'$gte': start.isoformat(), '$lte': end.isoformat()}
    }).sort([('time', -1)]))
    return {"status": "success", "data": data}

@app.get('/')
def api_home():
    return {"status": "success", "message": "Hello, World!"}
