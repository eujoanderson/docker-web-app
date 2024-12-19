# Atividade de Docker - Diego Pessoa

Neste desafio, você irá construir um ambiente completo de aplicação web utilizando Docker. O ambiente incluirá um servidor web Nginx, um banco de dados PostgreSQL e uma aplicação web simples. Você configurará e conectará todos os serviços para criar uma aplicação funcional.

#### 💻 Aqui abaixo tem um passo a passo de como foi configurado essa aplicação simples


A estrutura do projeto precisa ficar dessa forma.

![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/passo01.png)


Dentro de app, crie o arquivo app.py. 
```bash
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@postgres:5432/mydatabase'
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

![App Screenshot](https://github.com/eujoanderson/docker-web-app/blob/master/img/passo02.png)
