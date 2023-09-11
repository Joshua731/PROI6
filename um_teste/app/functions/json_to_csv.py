import json
import pandas as pd

# Carregue o JSON primário a partir de um arquivo (substitua 'seu_arquivo.json' pelo caminho do seu arquivo JSON)
with open(r'..\files\geojs-35-mun.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Acesse a lista de JSONs na chave 'features'
features = data['features']

# Crie um DataFrame do pandas a partir dos dados
df = pd.DataFrame(features)

# Extraia os valores das chaves 'id' e 'name' do DataFrame
df['id'] = df['properties'].apply(lambda x: x['id'])
df['name'] = df['properties'].apply(lambda x: x['name'])

# Selecione apenas as colunas 'id' e 'name'
df = df[['id', 'name']]

# Salve o DataFrame em um arquivo CSV (substitua 'saida.csv' pelo nome do arquivo de saída desejado)
df.to_csv(r'..\files\saida.csv', index=False)

print("Dados foram escritos em 'saida.csv'.")
