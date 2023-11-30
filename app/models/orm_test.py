import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

orindiuva = create_engine('sqlite:///F:/PROI6/database/orindiuva.db')
elias = create_engine('sqlite:///F:/PROI6/database/elias_fausto.db')
monte = create_engine('sqlite:///F:/PROI6/database/monte_alto.db')
paraguacu = create_engine('sqlite:///F:/PROI6/database/paraguacu.db')
rancharia = create_engine('sqlite:///F:/PROI6/database/rancharia.db')
suzano = create_engine('sqlite:///F:/PROI6/database/suzano.db')
tropeiros = create_engine('sqlite:///F:/PROI6/database/tropeiros.db')


class Usina(Base):
    __tablename__ = "Usina"

    id_usina = Column(Integer, primary_key=True)

    nome = Column(String(25))

    id_idgt = Column(Integer, ForeignKey("IDGT.id_idgt"))
    id_inv = Column(Integer, ForeignKey("Estado_Inversores.id_inv"))
    id_central = Column(Integer, ForeignKey("Central_Meteorologica.id_central"))
    timestamp = Column(DateTime, index=True, default=datetime.datetime.now())

    def __str__(self):
        return "Usina(id_usina={}, nome=\"{}\")".format(
            self.id_usina, self.nome)


class IDGT(Base):
    __tablename__ = "IDGT"

    id_idgt = Column(Integer, primary_key=True)

    valor = Column(Float)

    id_usina = relationship('Usina', backref='idgt')

    timestamp = Column(DateTime, default=datetime.datetime.now())


class Central_Meteorologica(Base):
    __tablename__ = "Central_Meteorologica"

    id_central = Column(Integer, primary_key=True)

    ISH = Column(Float)
    ISI = Column(Float)
    TA = Column(Float)
    TP = Column(Float)
    VV = Column(Float)
    DV = Column(Float)
    URA = Column(Float)
    PU = Column(Float)
    id_usina = relationship('Usina', backref='CM')
    timestamp = Column(DateTime, default=datetime.datetime.now())


class Estado_Inversores(Base):
    __tablename__ = "Estado_Inversores"

    id_inv = Column(Integer, primary_key=True)
    inv1 = Column(String(25))
    inv2 = Column(String(25))
    inv3 = Column(String(25))
    inv4 = Column(String(25))
    inv5 = Column(String(25))
    inv6 = Column(String(25))
    inv7 = Column(String(25))
    inv8 = Column(String(25))
    inv9 = Column(String(25))
    inv10 = Column(String(25))
    inv11 = Column(String(25))
    inv12 = Column(String(25))
    timestamp = Column(DateTime, default=datetime.datetime.now())

    id_usina = relationship('Usina', backref='inv')


class obra_cm_invs(Base):
    __tablename__ = "obra_cm_invs"

    id = Column(Integer, primary_key=True)
    estado_inv_id = Column(Integer, ForeignKey('Estado_Inversores.id_inv'))
    central_met_id = Column(Integer, ForeignKey('Central_Meteorologica.id_central'))
    usina = Column(String)
    # Relacionamentos com as tabelas Estado_Inversores e Central_Meteorologica
    estado_inv = relationship('Estado_Inversores')
    central_met = relationship('Central_Meteorologica')


Base.metadata.create_all(elias)
Base.metadata.create_all(monte)
Base.metadata.create_all(orindiuva)
Base.metadata.create_all(paraguacu)
Base.metadata.create_all(rancharia)
Base.metadata.create_all(suzano)
Base.metadata.create_all(tropeiros)
