from sqlalchemy import Integer, DateTime, ForeignKey, String
from datetime import datetime
from app.configs import db


class Quantidade(db.Model):
    __tablename__ = 'quantidade'

    id = db.Column(Integer, primary_key=True)
    quantidade = db.Column(Integer)
    tabela = db.Column(String)
    data = db.Column(DateTime, default=datetime.now())
    colunas_database_id = db.Column(Integer, ForeignKey('colunas_database.id_coluna'))
    colunas_database = db.relationship("ColunasDatabase", backref="quantidades")
