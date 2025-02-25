from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="/certs/key.pem",
        ssl_certfile="/certs/cert.pem"
    )
