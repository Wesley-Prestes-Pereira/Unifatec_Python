import json
import pandas as pd
import plotly.express as px
import streamlit as st

# Carregando o arquivo JSON
url = "https://raw.githubusercontent.com/Wesley-Prestes-Pereira/Unifatec_Python/main/P1/datasheet.json"
df = pd.read_json(url)

print(df.head())

# Função para converter duração para minutos
def convert_duration_to_minutes(duration):
    if 'min' in duration:
        return sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration.replace(' min', '').split(','))))
    return int(duration)

# Adicionando colunas de duração em minutos e tipo (filme ou série)
df['Duração_min'] = df['Duração'].apply(convert_duration_to_minutes)
df['Tipo'] = df['Duração_min'].apply(lambda x: 'Filme' if x <= 120 else 'Série')

# Criando o Dashboard com Streamlit
st.set_page_config(layout='wide')
st.title("Séries e Filmes")
st.sidebar.title('Filtros')

# Filtrando por classificação
filtro_classificacao = st.sidebar.multiselect('Classificação', df['Classificação'].unique())

if filtro_classificacao:
    df = df[df['Classificação'].isin(filtro_classificacao)]

# Exibindo o DataFrame e gráficos
st.dataframe(df)

st.plotly_chart(px.bar(df, x='Genero', title='Distribuição por Gênero'), use_container_width=True)
st.plotly_chart(px.bar(df, x='Classificação', y='Pontuação', title='Média de Pontuação por Classificação'), use_container_width=True)
st.plotly_chart(px.bar(df, x='Genero', y='Votos', title='Votos por Gênero'), use_container_width=True)
st.plotly_chart(px.bar(df, x='Classificação', y='Duração_min', title='Média de Duração por Classificação'), use_container_width=True)
