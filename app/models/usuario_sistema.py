from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from .bases_selecionadas import BasesSelecionadas
from ..configs import db
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class UsuarioSistema(db.Model, UserMixin):
    __tablename__ = 'usuario_sistema'

    id_login = db.Column(db.Integer, primary_key=True)
    id_db = db.Column(db.Integer, db.ForeignKey('bases_selecionadas.id_db'))
    nome_usuario = db.Column(db.String)
    nome_empresa = db.Column(db.String)
    email_login = db.Column(db.String)
    senha_login = db.Column(db.String)
    data_cadastro = db.Column(db.DateTime, default=datetime.now())
    base_selecionada = db.relationship("BasesSelecionadas", back_populates="usuarios")

    def set_password(self, password):
        self.senha_login = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_login, password)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id_login)
