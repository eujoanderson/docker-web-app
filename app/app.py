from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://joanderson:ifpb@postgres:5432/mydatabase'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
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
