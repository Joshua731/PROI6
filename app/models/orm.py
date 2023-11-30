import datetime
import time
import pymodbus.exceptions
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pymodbus.client.tcp import ModbusTcpClient, AsyncModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

URL_Or = "mysql+mysqlconnector://root:capua123@localhost:3306/orindiuva"
URL_EF = "mysql+mysqlconnector://root:capua123@localhost:3306/elias_fausto"
URL_PP = 'mysql+mysqlconnector://root:capua123@localhost:3306/paraguacu_paulista'
URL_MA = 'mysql+mysqlconnector://root:capua123@localhost:3306/monte_alto'
URL_Su = 'mysql+mysqlconnector://root:capua123@localhost:3306/suzano'
URL_Ta = 'mysql+mysqlconnector://root:capua123@localhost:3306/taubate'

orindiuva = 'sqlite:///F:/PROI6/database/orindiuva.db'
elias = 'sqlite:///F:/PROI6/database/elias_fausto.db'
monte = 'sqlite:///F:/PROI6/database/monte_alto.db'
paraguacu = 'sqlite:///F:/PROI6/database/paraguacu.db'
rancharia = 'sqlite:///F:/PROI6/database/rancharia.db'
suzano = 'sqlite:///F:/PROI6/database/suzano.db'
tropeiros = 'sqlite:///F:/PROI6/database/tropeiros.db'

# $ cd 'C:\Program Files\MySQL\MySQL Server 8.0\bin'
# $ .\mysql.exe -u root -p
# mysql> CREATE DATABASE ORM;
# mysql> USE ORM;
# mysql> SHOW TABLES;
Base = declarative_base()
c = 0

clienteor1 = ModbusTcpClient('45.176.175.27', port=1002)
clienteor2 = ModbusTcpClient('45.176.175.27', port=502)
clienteef1 = ModbusTcpClient('177.101.74.222', port=1002)
clienteef2 = ModbusTcpClient('177.101.74.222', port=502)
clientepp1 = ModbusTcpClient('191.242.49.24', port=1002)
clientema1 = ModbusTcpClient('45.170.209.104', port=1002)
clientesu = ModbusTcpClient('45.182.195.252', port=1002)


class Dados_da_Usina:
    def __init__(self, registros, usina, idgt, inversor):
        self.registros = registros
        self.usina = usina
        self.idgt = idgt
        self.inversor = inversor

    def get_regs(self, nome, reg):
        print('colhendo dados da central meteorológica')
        try:
            if reg is None:
                return None
            if nome == 'elias_fausto':
                val = clienteef1.read_holding_registers(reg, 2, slave=10)
                dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
                final = dec.decode_32bit_float()
                print(final)
                return final

            if nome == 'orindiuva':
                val = clienteor1.read_holding_registers(reg, 2, slave=10)
                dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
                final = dec.decode_32bit_float()
                print(final)
                return final

            if nome == 'monte_alto':
                if reg == 1 or reg == 3 or reg == 5 or reg == 9 or reg == 55:
                    val = clientema1.read_holding_registers(reg, 2, slave=1)
                    dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.LITTLE,
                                                             wordorder=Endian.BIG)
                    final = dec.decode_32bit_float()
                    print(final)

                    return final
                else:
                    val = clientema1.read_holding_registers(reg, 2, slave=1)
                    dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.BIG,
                                                             wordorder=Endian.LITTLE)
                    final = dec.decode_16bit_int()
                    print(final)

                    if final == 0:
                        return 'Em espera'
                    if final == 1:
                        return 'Gerando'
                    if final == 2:
                        return 'Falha'
                    if final == 3:
                        return 'Falha permanente'
                    if final == 6 or final == 4:
                        return 'Não encontrado'

            if nome == 'paraguacu_paulista':
                if reg == 1 or reg == 3 or reg == 5 or reg == 9 or reg == 55:
                    val = clientepp1.read_holding_registers(reg, 2, slave=1)
                    dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.LITTLE,
                                                             wordorder=Endian.BIG)
                    final = dec.decode_32bit_float()
                    print(final)

                    return final
                else:
                    val = clientepp1.read_holding_registers(reg, 2, slave=1)
                    dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.BIG,
                                                             wordorder=Endian.LITTLE)
                    final = dec.decode_16bit_int()
                    print(final)

                    if final == 0:
                        return 'Em espera'
                    if final == 1:
                        return 'Gerando'
                    if final == 2:
                        return 'Falha'
                    if final == 3:
                        return 'Falha permanente'
                    if final == 6 or final == 4:
                        return 'Não encontrado'
            if nome == "suzano":
                if reg == 1 or reg == 3 or reg == 5 or reg == 9 or reg == 55:
                    val = clientesu.read_holding_registers(reg, 2, slave=1)
                    dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.LITTLE,
                                                             wordorder=Endian.BIG)
                    final = dec.decode_32bit_float()
                    print(final)

                    return final
                else:
                    val = clientesu.read_holding_registers(reg, 2, slave=1)
                    dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.BIG,
                                                             wordorder=Endian.LITTLE)
                    final = dec.decode_16bit_int()
                    print(final)

                    if final == 0:
                        return 'Em espera'
                    if final == 1:
                        return 'Gerando'
                    if final == 2:
                        return 'Falha'
                    if final == 3:
                        return 'Falha permanente'
                    if final == 6 or final == 4:
                        return 'Não encontrado'

        except Exception as e:
            print(e)
            return 0

    def get_idgt(self):
        return None

    def get_invs(self, nome, inver):
        print('colhendo dados dos inversores')

        def invs(client):
            val = client.read_input_registers(5037, 2, slave=inver)
            dec = BinaryPayloadDecoder.fromRegisters(val.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
            final = dec.decode_32bit_uint()
            if final == 0:
                return "Em funcionamento"

            elif final == 4864:
                return "Chave de parada"

            elif final == 5376:
                return "Parada de emergência"

            elif final == 4608:
                return "Iniciando espera"

            elif final == 5120 or final == 5210:
                return "Em espera"

            elif final == 5632:
                return "Partindo"

            elif final == 9472:
                return "Falha de comunicação"

            elif final == 21760:
                return "Falha"

            elif final == 32768:
                return "Parado"

            elif final == 33024:
                return "Desclassificação"

            elif final == 33280:
                return "Expedição"

            elif final == 37120:
                return "Alarme ativo"

        try:
            if nome == 'elias_fausto':
                return invs(clienteef2)

            if nome == 'orindiuva':
                return invs(clienteor2)

            if nome == 'monte_alto':
                return invs(clientema1)

            if nome == 'paraguacu_paulista':
                return invs(clientepp1)

        except pymodbus.exceptions.ConnectionException as internet:
            print(internet)
            return 0
        except AttributeError as no_attr:
            print(no_attr)
            return 0

    def run(self, agora, url, u):
        engine = create_engine(url=url)
        # mysql> DESC Pessoa;

        Session = sessionmaker(engine, expire_on_commit=False)

        with engine.connect() as connection:
            try:
                with Session.begin() as session:
                    usina = Usina(nome=self.usina, timestamp=agora)
                    idgt = IDGT(valor=self.get_idgt(), timestamp=agora)
                    CM = Central_Meteorologica(ISH=self.get_regs(u, self.registros[0]),
                                               ISI=self.get_regs(u, self.registros[1]),
                                               TA=self.get_regs(u, self.registros[2]),
                                               TP=self.get_regs(u, self.registros[6]),
                                               DV=self.get_regs(u, self.registros[5]),
                                               VV=self.get_regs(u, self.registros[4]),
                                               URA=self.get_regs(u, self.registros[3]),
                                               PU=self.get_regs(u, self.registros[7]), timestamp=agora)
                    if u == "orindiuva" or u == 'elias_fausto':
                        inv = Estado_Inversores(inv1=self.get_invs(u, self.inversor[0]),
                                                inv2=self.get_invs(u, self.inversor[1]),
                                                inv3=self.get_invs(u, self.inversor[2]),
                                                inv4=self.get_invs(u, self.inversor[3]), timestamp=agora)
                        idgt.id_usina.append(usina)
                        CM.id_usina.append(usina)
                        inv.id_usina.append(usina)
                        session.add(usina)
                        pp = obra_cm_invs(usina=u, estado_inv_id=inv.id_inv, central_met_id=CM.id_central)
                        session.add(pp)

                    elif u == "monte_alto":
                        inv = Estado_Inversores(inv1=self.get_regs(u, self.registros[8]),
                                                inv2=self.get_regs(u, self.registros[9]),
                                                inv3=self.get_regs(u, self.registros[10]),
                                                inv4=self.get_regs(u, self.registros[11]),
                                                timestamp=agora)
                        pp = obra_cm_invs(usina=u, estado_inv_id=inv.id_inv, central_met_id=CM.id_central)
                        idgt.id_usina.append(usina)
                        CM.id_usina.append(usina)
                        inv.id_usina.append(usina)
                        session.add(usina)
                        session.add(pp)
                    else:
                        inv = Estado_Inversores(inv1=self.get_regs(u, self.registros[8]),
                                                inv2=self.get_regs(u, self.registros[9]),
                                                inv3=self.get_regs(u, self.registros[10]),
                                                inv4=self.get_regs(u, self.registros[11]),
                                                inv5=self.get_regs(u, self.registros[12]),
                                                inv6=self.get_regs(u, self.registros[13]),
                                                inv7=self.get_regs(u, self.registros[14]),
                                                inv8=self.get_regs(u, self.registros[15]),
                                                timestamp=agora)
                        idgt.id_usina.append(usina)
                        CM.id_usina.append(usina)
                        inv.id_usina.append(usina)
                        session.add(usina)
                        pp = obra_cm_invs(usina=u, estado_inv_id=inv.id_inv, central_met_id=CM.id_central)
                        session.add(pp)

            except pymodbus.exceptions.ConnectionException as internet:
                print(internet)
            except TypeError as vazio:
                print(vazio)


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


def roda(i):
    geral = {
        'usinas':
            [
                {
                    'nome':
                        'orindiuva',
                    'IP':
                        '45.176.175.27',
                    'holding_registers':
                        {
                            'registros':
                                [237, 223, 225, 227, 229, 231, 233, 405],
                            'unit_id':
                                10
                        },
                    'inversores':
                        [4, 1, 3, 2]
                },

                {
                    'nome':
                        'elias_fausto',
                    'IP':
                        '177.101.74.222',
                    'holding_registers':
                        {
                            'registros':
                                [223, 225, 227, 229, 231, 233, 235, 425],
                            'unit_id': 10,
                        },
                    'inversores':
                        [1, 2, 3, 4],
                },
                {
                    'nome':
                        'monte_alto',
                    'IP':
                        '45.170.209.104',
                    'holding_registers':
                        {
                            'registros':
                                [1, 3, 5, None, None, None, 9, 55, 157, 257, 357, 457],
                            'unit_id':
                                1
                        },

                    'inversores':
                        [1, 1, 1, 1]
                },
                {
                    'nome':
                        'paraguacu_paulista',
                    'IP':
                        '191.242.49.24',
                    'holding_registers':
                        {
                            'registros':
                                [1, 3, 5, None, None, None, 9, 55, 157, 257, 357, 457, 557, 657, 757, 857],
                            'unit_id':
                                1
                        },
                    'inversores':
                        [None],

                },
                {
                    'nome':
                        'suzano',
                    'IP':
                        '45.182.195.252',
                    'holding_registers':
                        {
                            'registros':
                                [1, 3, 5, None, None, None, 9, 55, 157, 257, 357, 457, 557, 657, 757, 857],
                            'unit_id':
                                1
                        },
                    'inversores':
                        [1, 1, 1, 1]
                },
                {
                    'nome':
                        'taubate',
                    'IP':
                        None,
                    'holding_registers':
                        {
                            'registros':
                                [None],
                            'unit_id':
                                None
                        },
                    'inversores':
                        [None]
                },
            ]
    }

    if i == 0:
        try:
            agora = datetime.datetime.now()
            registros = geral['usinas'][i]['holding_registers']['registros']
            usina = geral['usinas'][i]['nome']
            inv = geral['usinas'][i]['inversores']
            print(usina)

            bd = Dados_da_Usina(registros=registros, usina=usina, idgt=None, inversor=inv)
            bd.run(agora, orindiuva, usina)
        except TypeError as tipo:
            print(tipo)

    if i == 1:
        try:
            agora = datetime.datetime.now()
            registros = geral['usinas'][i]['holding_registers']['registros']
            usina = geral['usinas'][i]['nome']
            inv = geral['usinas'][i]['inversores']
            print(usina)

            bd = Dados_da_Usina(registros=registros, usina=usina, idgt=None, inversor=inv)
            bd.run(agora, elias, usina)
        except TypeError as tipo:
            print(tipo)

    if i == 2:
        try:
            agora = datetime.datetime.now()
            registros = geral['usinas'][i]['holding_registers']['registros']
            usina = geral['usinas'][i]['nome']
            inv = geral['usinas'][i]['inversores']
            print(usina)

            bd = Dados_da_Usina(registros=registros, usina=usina, idgt=None, inversor=inv)
            bd.run(agora, monte, usina)
        except TypeError as tipo:
            print(tipo)

    if i == 3:
        try:
            agora = datetime.datetime.now()
            registros = geral['usinas'][i]['holding_registers']['registros']
            usina = geral['usinas'][i]['nome']
            inv = geral['usinas'][i]['inversores']
            print(usina)

            bd = Dados_da_Usina(registros=registros, usina=usina, idgt=None, inversor=inv)
            bd.run(agora, paraguacu, usina)
        except TypeError as tipo:
            print(tipo)
    if i == 4:

        try:
            agora = datetime.datetime.now()
            registros = geral['usinas'][i]['holding_registers']['registros']
            usina = geral['usinas'][i]['nome']
            inv = geral['usinas'][i]['inversores']
            print(usina)

            bd = Dados_da_Usina(registros=registros, usina=usina, idgt=None, inversor=inv)
            bd.run(agora, suzano, usina)
        except TypeError as tipo:
            print(tipo)

    if i == 5:
        try:
            agora = datetime.datetime.now()
            registros = geral['usinas'][i]['holding_registers']['registros']
            usina = geral['usinas'][i]['nome']
            inv = geral['usinas'][i]['inversores']
            print(usina)

            bd = Dados_da_Usina(registros=registros, usina=usina, idgt=None, inversor=inv)
            bd.run(agora, suzano, usina)
        except TypeError as tipo:
            print(tipo)


if __name__ == "__main__":
    while True:
        try:
            for i in range(0, 5):
                roda(i)
                print("*" * 100)
                print("\n")
            print('descansando...')
            time.sleep(60)
        except Exception as e:
            print("Ocorreu um erro:", e)
            print("O programa será pausado por 1 minuto antes de retomar a execução.")
            time.sleep(60)  # Pausa o programa por 1 minuto (60 segundos)
