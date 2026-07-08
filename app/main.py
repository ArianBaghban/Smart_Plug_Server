from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import asyncio

from app.routers import devices
from app.routers import telemetry
from app.routers import commands
from app.routers import heartbeat
from app.routers import dashboard
from app.routers import auth

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

    while True:

        db = SessionLocal()

        try:
            check_offline_devices(db)

        finally:
            db.close()

        await asyncio.sleep(30)


@app.on_event("startup")
async def startup_event():

    mqtt_manager.start()

    asyncio.create_task(
        device_monitor_task()
    )


@app.on_event("shutdown")
async def shutdown_event():

    pass


app.include_router(devices.router)
app.include_router(telemetry.router)
app.include_router(commands.router)
app.include_router(heartbeat.router)
app.include_router(dashboard.router)
app.include_router(auth.router)


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