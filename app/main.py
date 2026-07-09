from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import asyncio

from app.routers import devices
from app.routers import telemetry
from app.routers import commands
from app.routers import heartbeat
from app.routers import dashboard
from app.routers import auth
from app.routers import websocket

from app.mqtt.manager import mqtt_manager

from app.database.session import SessionLocal
from app.services.device_monitor import check_offline_devices


app = FastAPI(
    title="Smart Plug IoT Server",
    description="Backend server for ESP32 smart plug devices",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def device_monitor_task():

    print("Device monitor task started")

    while True:

        print("Running device monitor...")

        db = SessionLocal()

        try:
            check_offline_devices(db)

        except Exception as e:
            print("Device monitor error:", e)

        finally:
            db.close()

        await asyncio.sleep(30)


@app.on_event("startup")
async def startup_event():

    print("Startup event executed")

    mqtt_manager.start()

    asyncio.create_task(device_monitor_task())


@app.on_event("shutdown")
async def shutdown_event():

    print("Server stopped")


app.include_router(devices.router)
app.include_router(telemetry.router)
app.include_router(commands.router)
app.include_router(heartbeat.router)
app.include_router(dashboard.router)
app.include_router(auth.router)
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {
        "service": "Smart Plug IoT Server",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }