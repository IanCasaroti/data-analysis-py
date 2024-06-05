# Importando a biblioteca pandas
import pandas as pd

# Carregando os dados
calendario_df = pd.read_csv('doc_1___desafio_individual.csv')
propriedades_df = pd.read_csv('doc_2___desafio_individual.csv')

# Removendo a string "00:00:00.000" das colunas de data
calendario_df['calendar_date'] = pd.to_datetime(calendario_df['calendar_date']).dt.date
calendario_df['creation_date'] = pd.to_datetime(calendario_df['creation_date']).dt.date


# Explorando os dados
print(calendario_df.head())
print(propriedades_df.head())

print(calendario_df.info())
print(propriedades_df.info())

print(calendario_df.describe())
print(propriedades_df.describe())



# Combinando os dados
dados_combinados_df = pd.merge(calendario_df, propriedades_df, on='property_id')
dados_combinados_df.to_csv('dados_combinados.csv', index=False)