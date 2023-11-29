from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.configs import db


class ColunasDatabase(db.Model):
    __tablename__ = 'colunas_database'

    id_coluna = db.Column(Integer, primary_key=True)
    database_id = db.Column(Integer, ForeignKey('database.id_db'))
    database = db.relationship("Database", backref="colunas")
    data = db.Column(DateTime, default=datetime.now())
    lista_colunas = db.Column(db.ARRAY(String))
