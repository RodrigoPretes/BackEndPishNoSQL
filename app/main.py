import uvicorn
from fastapi import FastAPI, Request
from database.db import create_tables
from api.endpoints.user import routes_user
from api.endpoints.sensores import routes_sensor
from services.mqtt_service import start_mqtt
import logging
import time

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Middleware para logar requisições e respostas
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log da requisição recebida
    logger.info(f"Requisição recebida: {request.method} {request.url}")

    # Se houver body na requisição (POST/PUT), tente logá-lo
    if request.method in ["POST", "PUT"]:
        body = await request.body()
        logger.info(f"Body da requisição: {body.decode('utf-8')}")

    # Executa a requisição e captura a resposta
    response = await call_next(request)

    # Log da resposta
    process_time = time.time() - start_time
    logger.info(f"Resposta: status {response.status_code} em {process_time:.2f}s")

    return response

# Registrar rotas
app.include_router(routes_user, prefix="/user")
app.include_router(routes_sensor, prefix="/sensores")

# Chamar a criação das tabelas
create_tables()

# Registrar a função startup_event como um evento de inicialização
@app.on_event("startup")
async def on_startup():
    start_mqtt()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
