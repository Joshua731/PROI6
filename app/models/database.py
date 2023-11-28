from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.configs import db


class Database(db.Model):
    __tablename__ = 'database'

    id_db = db.Column(Integer, primary_key=True)
    tipo_banco = db.Column(String)
    base_de_dados = db.Column(String)
    usuario_db = db.Column(String)
    senha_db = db.Column(String)
    ip = db.Column(String)
    porta = db.Column(Integer)
    data_insercao = db.Column(DateTime, default=datetime.now())
    usuario_id = db.Column(Integer, ForeignKey('usuario.id_login'))
    usuario = db.relationship("Usuario", backref="database")
