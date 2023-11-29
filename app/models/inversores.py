from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.configs import db


class Inversor(db.Model):
    __tablename__ = 'inversor'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    tabela = db.Column(String, nullable=True)
    numero = db.Column(Integer, nullable=True)
    correspondente = db.Column(String, nullable=True)
    data = db.Column(DateTime, default=datetime.now())

    # Coluna de chave estrangeira
    database_id = db.Column(Integer, ForeignKey('database.id_db'))
    database = relationship('Database')
