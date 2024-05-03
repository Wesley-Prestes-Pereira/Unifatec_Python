import json
import pandas as pd
import plotly.express as px
import streamlit as st

# Carrega o banco de dados JSON
url = "https://raw.githubusercontent.com/Wesley-Prestes-Pereira/Unifatec_Python/main/P1/datasheet.json"
data_json = json.loads(urlopen(url).read())
df = pd.DataFrame(data_json)

# Adaptações necessárias
def convert_duration_to_minutes(duration):
    if 'min' in duration:
        return sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration.replace(' min', '').split(','))))
    return int(duration)

df['Duração_min'] = df['Duração'].apply(convert_duration_to_minutes)
df['Tipo'] = df['Duração_min'].apply(lambda x: 'Filme' if x <= 120 else 'Série')

df_filmes = df[df['Tipo'] == 'Filme']
df_series = df[df['Tipo'] == 'Série']

# Definição das funções de gráficos
def distruibuicao_por_genero(df, title):
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

# Definição do layout do aplicativo
st.set_page_config(layout='wide')
st.title("Filmes/Séries: 🎥")
st.sidebar.title('Filtros')
filtro_classificacao = st.sidebar.multiselect('Classificação', df['Classificação'].unique())

if filtro_classificacao:
    df = df[df['Classificação'].isin(filtro_classificacao)]

aba1, aba2, aba3 = st.columns(3)
with aba1:
    st.plotly_chart(distruibuicao_por_genero(df_filmes, 'Filmes'), use_container_width=True)
    st.plotly_chart(pontuacao_por_classificacao(df_filmes, 'Filmes'), use_container_width=True)
with aba2:
    st.plotly_chart(votos_por_genero(df_filmes, 'Filmes'), use_container_width=True)
    st.plotly_chart(duracao_classificacao(df_filmes, 'Filmes'), use_container_width=True)
with aba3:
    st.plotly_chart(distruibuicao_por_genero(df_series, 'Séries'), use_container_width=True)
    st.plotly_chart(pontuacao_por_classificacao(df_series, 'Séries'), use_container_width=True)
    st.plotly_chart(votos_por_genero(df_series, 'Séries'), use_container_width=True)
    st.plotly_chart(duracao_classificacao(df_series, 'Séries'), use_container_width=True)
