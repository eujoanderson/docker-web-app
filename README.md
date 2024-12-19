# Atividade de Docker - Diego Pessoa

Neste desafio, você irá construir um ambiente completo de aplicação web utilizando Docker. O ambiente incluirá um servidor web Nginx, um banco de dados PostgreSQL e uma aplicação web simples. Você configurará e conectará todos os serviços para criar uma aplicação funcional.

#### 💻 Aqui abaixo tem um passo a passo de como foi configurado essa aplicação simples

Versão do linux utilizada:

![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/linux.png)

A estrutura do projeto precisa ficar dessa forma.

![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/passo01.png)

Primeirmente instale o docker na sua máquina.
```bash
apt install docker docker-compose
```



Dentro da pasta postgres crie o arquivo 'init.sql'. 
```bash
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie');
```

Depois crie o arquivo 'Dockerfile' para iniciar o banco.

```bash
FROM postgres:latest
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=joanderson
ENV POSTGRES_PASSWORD=ifpb
COPY init.sql /docker-entrypoint-initdb.d/
```

Rode o comando dentro da pasta Postgres
```bash
docker build .
```

Dentro da pasta app, crie o arquivo 'app.py'. 

![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/passo02.png)

```bash
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://joanderson:ifpb@postgres:5432/mydatabase'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return "Bem-vindo à minha aplicação web!"

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([u.name for u in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

Dentro do arquivo 'requiments.txt' adicione.

```bash
Flask
Flask-SQLAlchemy
psycopg2-binary
```

e Depois crie o 'Dockerfile'.

```bash
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

Rode o comando dentro da pasta app
```bash
docker build .
```

![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/passo03.png)


Dentro da pasta nginx crie.

nginx.conf
```bash
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

e Depois crie o 'Dockerfile'.

```bash
FROM nginx:latest
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

Rode o comando dentro da pasta app
```bash
docker build .
```

E por fim, crie o arquivo no diretório raiz do projeto.

```bash
version: '3'
services:
  nginx:
    build: ./nginx
    ports:
      - "8080:80"
    networks:
      - webnet

  app:
    build: ./app
    depends_on:
      - postgres
    networks:
      - webnet

  postgres:
    build: ./postgres
    environment:
      POSTGRES_PASSWORD: ifpb
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - webnet

volumes:
  pgdata:

networks:
  webnet:
```

e rode:

```
docker-compose up -d
```

![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/final.png)

A aplicação tem que funcionar normalmente:


```
http://<ip_server>:8080
```
![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/web-simples.png)


```bash
http://<ip_server>:8080/users/
```
![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/web_users.png)

