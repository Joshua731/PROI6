# import pandas as pd
# from sqlalchemy import create_engine
#
# # Carregar o arquivo CSV para um DataFrame
# file_path = 'app/geojsons/saida_atualizado.csv'
# data = pd.read_csv(file_path)
#
# # Configurações de conexão com o banco de dados
# # Substitua 'seu_banco_de_dados' e outras informações de acordo com o seu banco
#
# # Construir a string de conexão com o banco de dados usando SQLAlchemy
# connection_str = 'sqlite:///./database/database.db'
# engine = create_engine(connection_str)
#
# # Carregar os dados do DataFrame para o banco de dados como uma nova tabela
# table_name = 'cidades'  # Nome da tabela que será criada no banco de dados
#
# data.to_sql(table_name, engine, index=False, if_exists='replace')
# # O parâmetro if_exists='replace' irá substituir a tabela se ela já existir, use 'append' se quiser adicionar a uma tabela existente
#
#
#
# import pandas as pd
# from sqlalchemy import create_engine
#
# # Conectar-se ao banco de dados SQLite usando SQLAlchemy
# engine = create_engine('sqlite:///./database/database.db')
#
# # Ler a tabela do banco de dados para um DataFrame
# df = pd.read_sql('SELECT * FROM cidades', con=engine)
#
# # Atualizar os valores na coluna específica
# df['value'] = df['value'].replace(1, 0)
#
# # Gravar o DataFrame de volta para a tabela no banco de dados
# df.to_sql('cidades', con=engine, index=False, if_exists='replace')
#
# # Fechar a conexão
# engine.dispose()

import os


def procurar_arquivo(nome_arquivo, pasta_inicial='.'):
    caminho_completo = None

    for pasta_atual, subpastas, arquivos in os.walk(pasta_inicial):
        if nome_arquivo in arquivos:
            caminho_completo = os.path.join(pasta_atual, nome_arquivo)
            break  # Se encontrado, podemos interromper a busca

    return caminho_completo


# Exemplo de uso:
nome_arquivo_procurado = 'geojs-35-mun.json'
pasta_inicial = '.'  # Substitua pelo caminho da sua pasta

resultado = procurar_arquivo(nome_arquivo_procurado, pasta_inicial)

if resultado:
    print(f'O arquivo {nome_arquivo_procurado} foi encontrado em: {resultado}')
else:
    print(f'O arquivo {nome_arquivo_procurado} não foi encontrado na pasta especificada.')
