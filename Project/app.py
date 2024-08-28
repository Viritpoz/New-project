#!/usr/bin/env python3

from contextlib import asynccontextmanager
from datetime import datetime
import logging
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import pytz
from config.db import get_collection
from controllers.snmpcontroller import getsnmpdatacontroller, startup_event
import asyncio
import json
from bson import json_util
from service.snmpservie import get_today_data

logging.basicConfig(level=logging.INFO)
bangkok_tz = pytz.timezone('Asia/Bangkok')

pathenv = Path('./.env')
load_dotenv(dotenv_path=pathenv)
config = dotenv_values()  

collection = get_collection('snmp_data')

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Lifespan startup event triggered")
    await startup_event()
    yield
    logging.info("Lifespan shutdown event triggered")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Fetch the latest data
            latest_data = list(collection.find().sort([('time', -1)]).limit(1))
            # print(latest_data)
            if latest_data:
                # Convert to JSON-serializable format
                data_to_send = json.loads(json_util.dumps(latest_data[0]))
                await websocket.send_json(data_to_send)
            await asyncio.sleep(1)  # Wait for 1 second before sending next update
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()

@app.get('/today_snmp_data')
async def get_today_snmp_data():
    today_data = get_today_data()
    return {"status": "success", "data": json.loads(json_util.dumps(today_data))}

@app.websocket("/ws/today")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            today_data = get_today_data()
            await websocket.send_json(json.loads(json_util.dumps(today_data)))
            await asyncio.sleep(5)  # Update every 5 seconds
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()

@app.get('/latest_snmp_data')
async def get_latest_snmp_data():
    latest_data = list(collection.find().sort([('time', -1)]).limit(100))
    return {"status": "success", "data": json.loads(json_util.dumps(latest_data))}

@app.get('/snmp_data')
def get_snmp_data():
    return getsnmpdatacontroller()

@app.get('/snmp_data_range')
async def get_snmp_data_range(start_time: str, end_time: str):
    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    data = list(collection.find({
        'time': {'$gte': start.isoformat(), '$lte': end.isoformat()}
    }).sort([('time', -1)]))
    return {"status": "success", "data": json.loads(json_util.dumps(data))}

@app.get('/')
def api_home():
    return {"status": "success", "message": "Hello, World!"}