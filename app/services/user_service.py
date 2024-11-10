from fastapi import HTTPException
from core.auth import create_access_token, verify_password
from database.user import get_user_db
from fastapi import HTTPException
from core.auth import create_access_token

def authenticate_user(username: str, password: str):
    print(f"Buscando usuário {username} no banco de dados")  # Log do banco
    user = get_user_db(username)

    if not user:
        print("Usuário não encontrado no banco de dados")  # Log se o usuário não existir
        return None

    if not verify_password(password, user["password"]):
        print("Senha inválida")  # Log se a senha não corresponder
        return None

    print("Usuário autenticado com sucesso")  # Log de sucesso
    return user


def login_user(username: str, password: str):
    print(f"Autenticando usuário: {username}")  # Log do usuário

    user = authenticate_user(username, password)
    if not user:
        print("Usuário ou senha inválidos")  # Log do erro de autenticação
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Gera o token JWT
    token = create_access_token({"sub": user["username"]})
    print(f"Token gerado: {token}")  # Log do token gerado

    return {"access_token": token, "token_type": "bearer"}

