from datetime import datetime
from fastapi import HTTPException
from passlib.context import CryptContext
import logging
from uuid import uuid4
from models.users import User
from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("users")
logging.basicConfig(level=logging.INFO)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para gerar o hash da senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# database/user.py
def get_user_db(username: str):
    try:
        logging.info(f"Procurando usuário por username: {username}")
        response = table.query(
            IndexName='username-index',  # Nome do índice secundário
            KeyConditionExpression=Key('username').eq(username)
        )

        if not response["Items"]:
            logging.info("Usuário não encontrado.")
            return None

        logging.info(f"Usuário encontrado: {response['Items'][0]}")
        return response["Items"][0]  # Retorna o primeiro item encontrado

    except ClientError as e:
        logging.error(f"Erro ao buscar usuário: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar usuário: {e.response['Error']['Message']}"
        )

def validate_user_data(user: dict, required_fields: list):
    missing_fields = [field for field in required_fields if field not in user]
    if missing_fields:
        raise ValueError(f"Campos obrigatórios ausentes: {', '.join(missing_fields)}")

# Função create_user
def create_user(user: dict):
    try:
        validate_user_data(user, ["username", "password"])

        # Criptografa a senha
        user["password"] = hash_password(user["password"])

        # Cria uma instância do usuário e armazena no DynamoDB
        user_obj = User(**user)
        user_dict = user_obj.dict()
        table.put_item(Item=user_dict)
        
        logging.info(f"Usuário criado: {user}")
        return user

    except ClientError as e:
        logging.error(f"Erro ao criar usuário: {e}")
        return JSONResponse(content=e.response["Error"], status_code=500)

def get_user_byID(id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("id").eq(id)
        )
        user = response["Items"][0] if response["Items"] else None

        if user:
            user.pop("password", None)

        return user

    except ClientError as e:
        logging.error(f"Erro ao buscar usuário por ID: {e}")
        return JSONResponse(content=e.response["Error"], status_code=500)

def get_users():
    try:
        response = table.scan(
            Limit=5,
            ProjectionExpression="username, email, id"
        )
        return response["Items"]
    except ClientError as e:
        logging.error(f"Erro ao buscar usuários: {e}")
        return JSONResponse(content=e.response["Error"], status_code=500)

def delete_user(user_id: str, created_at: str):
    try:
        response = table.delete_item(
            Key={
                "id": user_id,
                "created_at": created_at
            }
        )
        logging.info(f"Usuário deletado: {user_id}")
        return response
    except ClientError as e:
        logging.error(f"Erro ao deletar usuário: {e}")
        return JSONResponse(content=e.response["Error"], status_code=500)

def update_user(user: dict):
    try:
        response = table.update_item(
            Key={
                "id": user["id"],
                "created_at": user["created_at"]
            },
            UpdateExpression="SET username = :username, age = :age",
            ExpressionAttributeValues={
                ":username": user["username"],
                ":age": user["age"]
            }
        )
        logging.info(f"Usuário atualizado: {user['id']}")
        return response
    except ClientError as e:
        logging.error(f"Erro ao atualizar usuário: {e}")
        return JSONResponse(content=e.response["Error"], status_code=500)
