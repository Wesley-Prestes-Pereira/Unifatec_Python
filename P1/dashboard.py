import json
import pandas as pd
import plotly.express as px
import streamlit as st

from urllib.request import urlopen

# URL do JSON
url = "https://raw.githubusercontent.com/Wesley-Prestes-Pereira/Unifatec_Python/main/P1/datasheet.json"
response = urlopen(url)
data_json = json.loads(response.read())
data = next(item for item in data_json if item['type'] == 'table')['data']
df = pd.DataFrame(data)

# Função para converter duração e classificar filmes/séries
def converter_duracao(duration):
    if 'min' in duration:
        return sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration.replace(' min', '').split(','))))
    return int(duration)

df['Duração_min'] = df['Duração'].apply(converter_duracao)
df['Tipo'] = df['Duração_min'].apply(lambda x: 'Filme' if x <= 120 else 'Série')

# Certifique-se de que as colunas usadas existem e têm dados
if 'Genero' not in df or 'Pontuação' not in df or 'Votos' not in df:
    st.error("Erro: Uma ou mais colunas necessárias não estão presentes no DataFrame.")
    st.stop()

# Filtros e configuração do Streamlit
filtro_classificacao = st.sidebar.multiselect('Filtrar por Classificação', options=df['Classificação'].unique())
filtro_genero = st.sidebar.multiselect('Filtrar por Gênero', options=df['Genero'].unique())
filtro_tipo = st.sidebar.radio('Selecionar Tipo', options=['Todos', 'Filme', 'Série'])

# Aplicação dos filtros
df_filtrado = df.copy()
if filtro_classificacao:
    df_filtrado = df_filtrado[df_filtrado['Classificação'].isin(filtro_classificacao)]
if filtro_genero:
    df_filtrado = df_filtrado[df_filtrado['Genero'].isin(filtro_genero)]
if filtro_tipo != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Tipo'] == filtro_tipo]

# Abas para visualização dos dados
aba1, aba2, aba3, aba4 = st.tabs(['Dataset', 'Filmes', 'Séries', 'Análise Detalhada'])
with aba1:
    st.dataframe(df)
with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(criar_grafico_barra(df[df['Tipo'] == 'Filme'], 'Genero', 'Pontuação', 'Distribuição de Pontuação por Gênero - Filmes', {'Genero': 'Gênero', 'Pontuação': 'Pontuação Média'}), use_container_width=True)
        st.plotly_chart(criar_grafico_barra(df[df['Tipo'] == 'Filme'], 'Genero', 'Votos', 'Votos por Gênero - Filmes', {'Genero': 'Gênero', 'Votos': 'Total de Votos'}), use_container_width=True)
    with coluna2:
        st.plotly_chart(criar_grafico_linha(df[df['Tipo'] == 'Filme'], 'Classificação', 'Duração_min', 'Duração por Classificação - Filmes', {'Classificação': 'Classificação', 'Duração_min': 'Duração Média (min)'}), use_container_width=True)
        st.plotly_chart(criar_grafico_linha(df[df['Tipo'] == 'Filme'], 'Genero', 'Pontuação', 'Evolução da Pontuação por Gênero - Filmes', {'Genero': 'Gênero', 'Pontuação': 'Pontuação Média'}), use_container_width=True)
with aba3:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(criar_grafico_barra(df[df['Tipo'] == 'Série'], 'Genero', 'Pontuação', 'Distribuição de Pontuação por Gênero - Séries', {'Genero': 'Gênero', 'Pontuação': 'Pontuação Média'}), use_container_width=True)
        st.plotly_chart(criar_grafico_barra(df[df['Tipo'] == 'Série'], 'Genero', 'Votos', 'Votos por Gênero - Séries', {'Genero': 'Gênero', 'Votos': 'Total de Votos'}), use_container_width=True)
    with coluna2:
        st.plotly_chart(criar_grafico_linha(df[df['Tipo'] == 'Série'], 'Classificação', 'Duração_min', 'Duração por Classificação - Séries', {'Classificação': 'Classificação', 'Duração_min': 'Duração Média (min)'}), use_container_width=True)
        st.plotly_chart(criar_grafico_linha(df[df['Tipo'] == 'Série'], 'Genero', 'Pontuação', 'Evolução da Pontuação por Gênero - Séries', {'Genero': 'Gênero', 'Pontuação': 'Pontuação Média'}), use_container_width=True)
with aba4:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(criar_grafico_dispersao(df, 'Votos', 'Pontuação', 'Genero', 'Relação Votos-Pontuação por Gênero', {'Votos': 'Votos', 'Pontuação': 'Pontuação', 'Genero': 'Gênero'}), use_container_width=True)
    with coluna2:
        st.plotly_chart(criar_grafico_linha(df, 'Genero', 'Pontuação', 'Evolução da Pontuação por Gênero', {'Genero': 'Gênero', 'Pontuação': 'Pontuação Média'}), use_container_width=True)

