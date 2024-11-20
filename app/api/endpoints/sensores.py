from fastapi import APIRouter, HTTPException, Depends, status
from app.database.sensor import fetch_sensor_data  
from fastapi.security import OAuth2PasswordBearer
from app.core.auth import decode_access_token

routes_sensor = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

# Endpoint para visualizar os dados no DynamoDB
@routes_sensor.get("/sensodata", summary="Get Sensor Data", description="GET valor do sensor com base no nome informado")
async def get_sensor_data(sensor: str, token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        response = fetch_sensor_data(sensor)  
        if response is None:
            raise HTTPException(status_code=404, detail="Sensor não encontrado")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@routes_sensor.get("/sensordata/umidade", summary="GET Sensor Umidity", description="GET valor sensor de umidade")
async def get_sensor_data(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        response = fetch_sensor_data("UMIDADE")  
        if response is None:
            raise HTTPException(status_code=404, detail="Sensor não encontrado")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@routes_sensor.get("/sensordata/temperatura", summary="GET Sensor temperature", description="GET valor sensor de temperatura")
async def get_sensor_data(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        response = fetch_sensor_data("TEMPERATURA")  
        if response is None:
            raise HTTPException(status_code=404, detail="Sensor não encontrado")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routes_sensor.get("/sensordata/monoxido", summary="GET Sensor monoxide", description="GET valor sensor de monoxido")
async def get_sensor_data(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        response = fetch_sensor_data("MONOXIDO")  
        if response is None:
            raise HTTPException(status_code=404, detail="Sensor não encontrado")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routes_sensor.get("/sensordata/dioxido", summary="GET Sensor Dioxide", description="GET valor sensor de Dioxido")
async def get_sensor_data(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        response = fetch_sensor_data("DIOXIDO")  
        if response is None:
            raise HTTPException(status_code=404, detail="Sensor não encontrado")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    