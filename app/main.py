import uvicorn
from fastapi import FastAPI, Request
from app.database.db import create_tables
from app.api.endpoints.user import routes_user
from app.api.endpoints.sensores import routes_sensor
from app.services.mqtt_service import start_mqtt
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title = "Clean Air - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

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
app.include_router(routes_sensor, prefix="/sensores", tags=["Sensores"])
app.include_router(routes_user, prefix="/user", tags=["Rotas de usuário"])

# Chamar a criação das tabelas
create_tables()

# Registrar a função startup_event como um evento de inicialização
@app.on_event("startup")
async def on_startup():
    start_mqtt()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
