#!/usr/bin/env python3

from contextlib import asynccontextmanager
from datetime import datetime
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import pytz
from config.db import get_collection
from controllers.snmpcontroller import getsnmpdatacontroller, startup_event
import asyncio
import json
from bson import json_util
from service.snmpservie import count_student_frombuilding, count_student_frombuilding_floor, get_today_data, getDatafromBuilding
from starlette.websockets import WebSocketState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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
    logger.info("New WebSocket connection established")
    
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            today_data = get_today_data()
            json_data = json.loads(json_util.dumps(today_data))

            # Check if websocket is still open before sending
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json(json_data)
                logger.debug(f"Sent data: {json_data}")
            else:
                logger.info("WebSocket connection is closed, stopping sending data.")
                break

            await asyncio.sleep(5)  # Update every 5 seconds

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except asyncio.CancelledError:
        logger.info("WebSocket connection cancelled")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
        logger.info("WebSocket connection closed")

@app.websocket("/ws/today/{building}")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("New WebSocket connection established")
    try:
        while True:
            if websocket.client_state == WebSocketState.DISCONNECTED:
                logger.info("Client disconnected")
                break

            today_data = getDatafromBuilding(buildingname=websocket.path_params['building'])
            json_data = json.loads(json_util.dumps(today_data))
            await websocket.send_json(json_data)
            logger.debug(f"Sent data: {json_data}")
            
            await asyncio.sleep(5)  # Update every 5 seconds

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except asyncio.CancelledError:
        logger.info("WebSocket connection cancelled")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
        logger.info("WebSocket connection closed")

@app.websocket("/ws/today/total/{building}")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("New WebSocket connection established")
    try:
        while True:
            if websocket.client_state == WebSocketState.DISCONNECTED:
                logger.info("Client disconnected")
                break
             # Receive a message as bytes
            total_today_data = count_student_frombuilding(buildingname=websocket.path_params['building'])
            floor_todat_data = count_student_frombuilding_floor(buildingname=websocket.path_params['building'])
            json_data = json.loads(json_util.dumps({"total": total_today_data, "floor": floor_todat_data}))
            await websocket.send_json(json_data)
            logger.debug(f"Sent data: {json_data}")
            
            await asyncio.sleep(5)  # Update every 5 seconds

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except asyncio.CancelledError:
        logger.info("WebSocket connection cancelled")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
        logger.info("WebSocket connection closed")

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