import json
import pandas as pd
import plotly.express as px
import streamlit as st
from urllib.request import urlopen

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

st.set_page_config(layout='wide')
st.title("IMDB de Filmes e Séries 🎥")

filtro_genero = st.sidebar.multiselect('Filtrar por Gênero', options=df['Genero'].unique())
filtro_classificacao = st.sidebar.multiselect('Filtrar por Classificação', options=df['Classificação'].unique())
filtro_tipo = st.sidebar.radio('Selecionar Tipo', ['Todos', 'Filme', 'Série'])

df_filtrado = df.copy()
if filtro_genero:
    df_filtrado = df_filtrado[df_filtrado['Genero'].isin(filtro_genero)]
if filtro_classificacao:
    df_filtrado = df_filtrado[df_filtrado['Classificação'].isin(filtro_classificacao)]
if filtro_tipo != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Tipo'] == filtro_tipo]

aba1, aba2, aba3, aba4 = st.tabs(['Dataset', 'Filmes', 'Séries', 'Análise Detalhada'])
with aba1:
    st.dataframe(df_filtrado)
with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(distribuicao_por_genero(df_filtrado[df_filtrado['Tipo'] == 'Filme'], 'Filmes'), use_container_width=True)
        st.plotly_chart(pontuacao_por_classificacao(df_filtrado[df_filtrado['Tipo'] == 'Filme'], 'Filmes'), use_container_width=True)
    with coluna2:
        st.plotly_chart(votos_por_genero(df_filtrado[df_filtrado['Tipo'] == 'Filme'], 'Filmes'), use_container_width=True)
        st.plotly_chart(duracao_classificacao(df_filtrado[df_filtrado['Tipo'] == 'Filme'], 'Filmes'), use_container_width=True)
with aba3:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(distribuicao_por_genero(df_filtrado[df_filtrado['Tipo'] == 'Série'], 'Séries'), use_container_width=True)
        st.plotly_chart(pontuacao_por_classificacao(df_filtrado[df_filtrado['Tipo'] == 'Série'], 'Séries'), use_container_width=True)
    with coluna2:
        st.plotly_chart(votos_por_genero(df_filtrado[df_filtrado['Tipo'] == 'Série'], 'Séries'), use_container_width=True)
        st.plotly_chart(duracao_classificacao(df_filtrado[df_filtrado['Tipo'] == 'Série'], 'Séries'), use_container_width=True)
with aba4:
        st.plotly_chart(px.scatter(df_filtrado, x='Pontuação', y='Votos', color='Genero', title='Relação Votos-Pontuação'), use_container_width=True)

