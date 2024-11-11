# Use uma imagem base do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /

# Copie o requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie o restante do código para o container
COPY . .

# Expõe a porta em que a aplicação irá rodar
EXPOSE 443

# Define o comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "443"]
