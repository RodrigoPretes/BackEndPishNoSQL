from fastapi import APIRouter, HTTPException
from database.sensor import fetch_sensor_data  # Importando a função correta

routes_sensor = APIRouter()

# Endpoint para visualizar os dados no DynamoDB
@routes_sensor.get("/sensordata")
async def get_sensor_data(sensor: str):
    try:
        response = fetch_sensor_data(sensor)  # Chama a função correta
        if response is None:
            raise HTTPException(status_code=404, detail="Sensor não encontrado")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
