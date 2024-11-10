from fastapi import APIRouter
from models.users import User, UserCreate, UserDelete
from database.user import *
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from services.user_service import login_user
from core.auth import decode_access_token


routes_user = APIRouter()

# Definindo o tokenUrl corretamente (sem barra inicial)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

@routes_user.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Username: {form_data.username}, Password: {form_data.password}")  # Debug
    response = login_user(form_data.username, form_data.password)
    print(f"Login response: {response}")  # Debug
    return response


@routes_user.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"user": payload["sub"]}

#Criar usuario
@routes_user.post("/create", response_model=User, summary="Create User", description="Rota Responsável pela criação de um usuário")
def create(user: UserCreate):
    return create_user(user.model_dump())

@routes_user.get("/get/{id}")
def get_by_id(id: str):
    print(id)
    return get_user_byID(id)

@routes_user.get("/all")
def get_all():
    return get_users()

@routes_user.delete("/delete")
def delete(user: UserDelete):
    return delete_user(user.model_dump())


@routes_user.patch("/update")
def update(user: UserCreate):
    return update_user(user.model_dump())