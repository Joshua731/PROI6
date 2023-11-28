from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.configs import db


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_login = db.Column(Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(String)
    nome_empresa = db.Column(String)
    email_login = db.Column(String)
    senha_login = db.Column(String)
    data_cadastro = db.Column(DateTime, default=datetime.now())
