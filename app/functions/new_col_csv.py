import pandas as pd

# Carregue o CSV existente
df = pd.read_csv(r'..\files\saida.csv', encoding='utf-8')

# Adicione a coluna 'value' com o valor 1 para a cidade de Jacareí e 0 para todas as outras cidades
df['value'] = df['name'].apply(lambda x: 1 if x == 'Jacareí' else 0)

# Salve o DataFrame atualizado em um novo arquivo CSV
df.to_csv(r'..\files\saida_atualizado.csv', index=False)

print("CSV atualizado foi salvo como 'saida_atualizado.csv'.")