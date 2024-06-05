import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('dados_combinados.csv')

# Remover a string "00:00:00.000" das colunas de data
df['calendar_date'] = df['calendar_date'].str.replace(' 00:00:00.000', '')
df['creation_date'] = df['creation_date'].str.replace(' 00:00:00.000', '')

# Salvar o DataFrame de volta para um arquivo CSV
df.to_csv('dados_combinados.csv', index=False)