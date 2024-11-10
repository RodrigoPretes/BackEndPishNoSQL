import logging
from os import getenv
from datetime import datetime
import boto3
from paho.mqtt.client import Client
from dotenv import load_dotenv
import json
from decimal import Decimal, InvalidOperation

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Broker MQTT
BROKER = getenv("MQTT_BROKER", "test.mosquitto.org")
PORT = int(getenv("MQTT_PORT", "1883"))
USERNAME = getenv("MQTT_USERNAME")
PASSWORD = getenv("MQTT_PASSWORD")
CLIENT_ID = getenv("MQTT_CLIENT_ID", "unique-client-id")
TOPICS = ["UMIDADE", "TEMPERATURA", "MONOXIDO", "DIOXIDO"]

# Configuração do DynamoDB
DYNAMO_DB_ENDPOINT = getenv("DYNAMO_DB_ENDPOINT", "http://localhost:8001")
AWS_REGION = getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY", "test")

# Configuração do cliente DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    endpoint_url=DYNAMO_DB_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
table = dynamodb.Table('SensorData')  # Nome da tabela

# Inicialização do cliente MQTT e sinalizador global
mqtt_client = Client(client_id=CLIENT_ID)
mqtt_started = False  # Sinalizador para evitar reinicialização do MQTT

# Callback ao conectar no broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conectado ao broker MQTT com sucesso.")
        for topic in TOPICS:
            client.subscribe(topic)
            logging.info(f"Inscrito no tópico: {topic}")
    else:
        logging.error(f"Falha ao conectar ao broker MQTT. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    try:
        # Decodificar o payload recebido
        payload = msg.payload.decode().strip()
        
        # Inicializar a variável de valor
        value = None
        
        # Verificar se o payload é uma string que representa JSON
        if payload.startswith('{') and payload.endswith('}'):
            data_json = json.loads(payload)
            # Extrair o valor baseado no tópico da mensagem
            if msg.topic in data_json:
                value = Decimal(str(data_json[msg.topic]))
            else:
                logging.error(f"Tópico {msg.topic} não encontrado no JSON recebido.")
                return
        else:
            # Tentar converter diretamente para Decimal se não for JSON
            value = Decimal(payload)

        # Preparar dados para inserir no DynamoDB
        data = {
            "sensor": msg.topic,
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Inserção no DynamoDB
        table.put_item(Item=data)
        logging.info(f"Dados inseridos no DynamoDB: {data}")

    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar o JSON: {payload}")
    except KeyError as ke:
        logging.error(f"Erro ao acessar chave no payload JSON: {ke}")
    except InvalidOperation as e:
        logging.error(f"Erro ao converter payload para Decimal: {payload}")
    except Exception as e:
        logging.error(f"Erro ao processar mensagem MQTT: {e}")

# Configuração dos callbacks
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Função para iniciar a conexão MQTT
def start_mqtt():
    global mqtt_started
    if not mqtt_started:
        try:
            mqtt_client.connect(BROKER, PORT)
            mqtt_client.loop_start()
            mqtt_started = True  # Define como iniciado para evitar múltiplas conexões
            logging.info("Serviço MQTT iniciado e aguardando mensagens.")
        except Exception as e:
            logging.error(f"Erro ao conectar ao broker MQTT: {e}")
