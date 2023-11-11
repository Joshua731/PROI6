from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class BasesSelecionadas(Base):
    __tablename__ = 'bases_selecionadas'

    id_db = Column(Integer, primary_key=True)
    base_de_dados = Column(String)
    usuario_db = Column(String)
    senha_db = Column(String)
    IP = Column(String)
    Porta = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now)
    usuarios = relationship("UsuarioSistema", back_populates="base_selecionada")
