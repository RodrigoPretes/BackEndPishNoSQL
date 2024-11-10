from boto3 import resource
from botocore.exceptions import ClientError
from os import getenv
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = getenv("AWS_REGION", "us-east-1")
DYNAMO_DB_ENDPOINT = getenv("DYNAMO_DB_ENDPOINT", "http://localhost:8001")
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY", "test")

dynamodb = resource(
    'dynamodb',
    endpoint_url=DYNAMO_DB_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def table_exists(table_name: str):
    """Verifica se a tabela já existe no DynamoDB."""
    try:
        dynamodb.meta.client.describe_table(TableName=table_name)
        print(f"Tabela '{table_name}' já existe.")
        return True
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        return False

def create_tables():
    """Cria as tabelas 'users' e 'SensorData' com índices secundários apenas se não existirem."""
    
    # Tabela de usuários
    if not table_exists("users"):
        try:
            users_table = dynamodb.create_table(
                TableName="users",
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"},  # Chave primária
                ],
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"},  # ID como string
                    {"AttributeName": "username", "AttributeType": "S"}  # Definição do índice
                ],
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "username-index",  # Nome do índice
                        "KeySchema": [
                            {"AttributeName": "username", "KeyType": "HASH"}
                        ],
                        "Projection": {
                            "ProjectionType": "ALL"  # Retorna todos os atributos
                        }
                    }
                ],
                BillingMode="PAY_PER_REQUEST"
            )
            users_table.meta.client.get_waiter("table_exists").wait(TableName="users")
            print("Tabela 'users' criada com sucesso!")
        except ClientError as e:
            print(f"Erro ao criar tabela 'users': {e.response['Error']['Message']}")

    # Tabela de dados dos sensores
    if not table_exists("SensorData"):
        try:
            sensor_table = dynamodb.create_table(
                TableName="SensorData",
                KeySchema=[
                    {"AttributeName": "sensor", "KeyType": "HASH"},  # Tipo de sensor como chave primária
                    {"AttributeName": "timestamp", "KeyType": "RANGE"}  # Timestamp como chave de ordenação
                ],
                AttributeDefinitions=[
                    {"AttributeName": "sensor", "AttributeType": "S"},
                    {"AttributeName": "timestamp", "AttributeType": "S"}
                ],
                BillingMode="PAY_PER_REQUEST"
            )
            sensor_table.meta.client.get_waiter("table_exists").wait(TableName="SensorData")
            print("Tabela 'SensorData' criada com sucesso!")
        except ClientError as e:
            print(f"Erro ao criar tabela 'SensorData': {e.response['Error']['Message']}")
