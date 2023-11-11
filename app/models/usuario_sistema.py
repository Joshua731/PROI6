from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from .bases_selecionadas import BasesSelecionadas

Base = declarative_base()


class UsuarioSistema(Base):
    __tablename__ = 'usuario_sistema'

    id_login = Column(Integer, primary_key=True)
    id_db = Column(Integer, ForeignKey('bases_selecionadas.id_db'))
    nome_usuario = Column(String)
    nome_empresa = Column(String)
    email_login = Column(String)
    senha_login = Column(String)
    data_cadastro = Column(DateTime, default=datetime.now)
    base_selecionada = relationship("BasesSelecionadas", back_populates="usuarios")
