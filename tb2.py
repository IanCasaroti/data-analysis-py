# Importando as bibliotecas necessárias
import pandas as pd
import plotly.express as px

# Carregando os dados
df = pd.read_csv('dados_combinados.csv')

# Filtrar os dados para o mês e ano especificados
df_mes = df[(df['calendar_date'].dt.year == ano) & (df['calendar_date'].dt.month == mes)]

# Pivotar os dados para que cada propriedade seja uma linha e cada data seja uma coluna
df_pivot = df_mes.pivot(index='property_id', columns='calendar_date', values='last_daily_price')

# Substituir os valores de preço pelos status de ocupação
df_pivot = df_pivot.replace(df_mes.set_index('calendar_date')['occupancy'].to_dict())

# Criar um mapa de calor do calendário
fig = px.imshow(df_pivot, color_continuous_scale='RdYlGn', labels=dict(color="Occupancy Status"))
fig.show()
