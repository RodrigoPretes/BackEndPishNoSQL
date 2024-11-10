Para rodar a aplicação é necessário ter o dynamodb instalado localmente na sua maquina

após instalado, extraia o arquivo .zip da aws e execute ele na sua maquina com o seguinte comando 

````
java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar -port 8001
````

no meu caso, precisei utilizar a porta 8001, mas por padrão ele na inicializa na porta 8000 

Além disso, é necessário possuir o jdk mais recente instalado na sua maquina

Após instanciar o banco de dados na sua maquina, é necessario ter o python mais recente instalado na sua maquina 

criar um venv para conseguir trabalhar com o python, rode o seguinte comando 

````
python venv venv 

````

````
.venv\Scripts\activate
````

instalar todas as bibliotecas necessarias para iniciar o projeto 


````

pip install -r requirements.txt

````


e por fim, iniciar a aplicação com o seguinte comando

````

uvicorn main:app --reload --port 2087

````
