from sqlalchemy import Integer, String, DateTime, ForeignKey, Column
from datetime import datetime
from app.configs import db


class Bancos(db.Model):
    __tablename__ = 'bancos'

    id_banco = db.Column(Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(String)
    base = db.Column(String)
    user = db.Column(String)
    pwd = db.Column(String)
    ip = db.Column(String)
    port = db.Column(Integer)
    date = db.Column(DateTime, default=datetime.now())
