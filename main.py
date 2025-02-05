from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.ParticulateMatterController import ParticulateMatterRestController
from controllers.CO2_Temp_Humidity import CO2TempHumidityController

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pm_rest_controller = ParticulateMatterRestController()
co2_temp_humidty_controller = CO2TempHumidityController()

app.include_router(pm_rest_controller.router)
app.include_router(co2_temp_humidty_controller.router)

