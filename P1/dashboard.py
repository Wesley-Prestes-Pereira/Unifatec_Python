import json
import pandas as pd
import plotly.express as px
import streamlit as st
from urllib.request import urlopen

# URL do seu JSON no GitHub
url = "https://raw.githubusercontent.com/Wesley-Prestes-Pereira/Unifatec_Python/main/P1/datasheet.json"
response = urlopen(url)
data_json = json.loads(response.read())
data = next(item for item in data_json if item['type'] == 'table')['data']
df = pd.DataFrame(data)

def convert_duration_to_minutes(duration):
    if 'min' in duration:
        return sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration.replace(' min', '').split(','))))
    return int(duration)

df['Duração_min'] = df['Duração'].apply(convert_duration_to_minutes)
df['Tipo'] = df['Duração_min'].apply(lambda x: 'Filme' if x <= 120 else 'Série')

# Separando filmes e séries
df_filmes = df[df['Tipo'] == 'Filme']
df_series = df[df['Tipo'] == 'Série']

# Funções para criação de gráficos
def distribuicao_por_genero(df, title):
    fig = px.bar(df, x='Genero', title=f'{title} - Distribuição por Gênero')
    return fig

def pontuacao_por_classificacao(df, title):
    fig = px.bar(df, x='Classificação', y='Pontuação', title=f'{title} - Média de Pontuação por Classificação')
    return fig

def votos_por_genero(df, title):
    fig = px.bar(df, x='Genero', y='Votos', title=f'{title} - Votos por Gênero')
    return fig

def duracao_classificacao(df, title):
    fig = px.bar(df, x='Classificação', y='Duração_min', title=f'{title} - Média de Duração por Classificação')
    return fig

# Configurações do Streamlit
st.set_page_config(layout='wide')
st.title("Análise de Filmes e Séries 🎥")

filtro_classificacao = st.sidebar.multiselect('Filtrar por Classificação', df['Classificação'].unique())

if filtro_classificacao:
    df = df[df['Classificação'].isin(filtro_classificacao)]

aba1, aba2, aba3 = st.tabs(['Dataset', 'Filmes', 'Séries'])
with aba1:
    st.dataframe(df)
with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(distribuicao_por_genero(df_filmes, 'Filmes'), use_container_width=True)
        st.plotly_chart(pontuacao_por_classificacao(df_filmes, 'Filmes'), use_container_width=True)
    with coluna2:
        st.plotly_chart(votos_por_genero(df_filmes, 'Filmes'), use_container_width=True)
        st.plotly_chart(duracao_classificacao(df_filmes, 'Filmes'), use_container_width=True)
with aba3:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(distribuicao_por_genero(df_series, 'Séries'), use_container_width=True)
        st.plotly_chart(pontuacao_por_classificacao(df_series, 'Séries'), use_container_width=True)
    with coluna2:
        st.plotly_chart(votos_por_genero(df_series, 'Séries'), use_container_width=True)
        st.plotly_chart(duracao_classificacao(df_series, 'Séries'), use_container_width=True)
