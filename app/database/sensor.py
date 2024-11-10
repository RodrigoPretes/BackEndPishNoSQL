from datetime import datetime
from fastapi import HTTPException
from passlib.context import CryptContext
import logging
from uuid import uuid4
from models.sensor import GetSensor, Sensor
from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("SensorData")
logging.basicConfig(level=logging.INFO)

# database/user.py
def fetch_sensor_data(sensor: str):
    try:
        logging.info(f"Procurando Sensor com nome de: {sensor}")
        response = table.query(
            KeyConditionExpression=Key('sensor').eq(sensor)
        )

        if not response["Items"]:
            logging.info("Sensor não encontrado.")
            return None

        logging.info(f"Sensor encontrado: {response['Items'][0]}")
        return response["Items"]

    except ClientError as e:
        logging.error(f"Erro ao buscar Sensor: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar Sensor: {e.response['Error']['Message']}"
        )

def get_all_sensores():
    try:
        response = table.scan(
            Limit=15,
        )
        return response["Items"]
    except ClientError as e:
        logging.error(f"Erro ao buscar Sensor: {e}")
        return JSONResponse(content=e.response["Error"], status_code=500)
    



