
# Importação das Bibliotecas necessárias para o projeto.
import json
import urllib
import pandas as pd
from urllib.request import urlopen
import plotly.express as px
import streamlit as st

# Baixa um arquivo JSON (A base de dados) a partir da URL fornecida.
url = "https://raw.githubusercontent.com/guilherme-wagner/python/main/netflix.json"
response = urlopen(url) # Abre a URL e obtém a resposta.
data_json = json.loads(response.read()) # Carrega os dados JSON da resposta.
df = pd.DataFrame.from_dict(data_json) # Converte os dados JSON em um Dataframe pandas.
print(df) # Imprime na tela o dataframe.

# Ordenando o Dataframe pelas avaliações
df_sorted_by_rating = df.sort_values(by='rating')
print(df_sorted_by_rating)

# Ordeando o Dataframe pelos votos
df_sorted_by_votes = df.sort_values(by='votes', ascending=False)
print(df_sorted_by_votes)

#Gráfico das séries mais avaliadas
grafico_mais_avaliadas = px.bar(
df_sorted_by_rating.tail(5),
x = 'lister-item-header',
y = 'rating',
text_auto = True,
title = 'TOP 5 séries + avaliadas',
labels= {'rating': 'Avaliação', 'lister-item-header': 'Nome da série'}
)
grafico_mais_avaliadas.show()

#Gráfico das séries menos avaliadas
grafico_menos_avaliadas = px.bar(
  df_sorted_by_rating.head(5),
  x = 'lister-item-header',
  y = 'rating',
  text_auto = True,
  title = 'TOP 5 séries - avaliadas',
  labels= {'rating': 'Avaliação da série', 'lister-item-header': 'Nome da série'}
)
grafico_menos_avaliadas.show()

#Gráfico dos gêneros mais votados
df_genre_split = df.assign(genre=df['genre'].str.split(', ')).explode('genre')
df_genre_votes = df_genre_split.groupby('genre')['votes'].sum().reset_index()
grafico_generos_votados = px.bar(
    df_genre_votes,
    x='genre',
    y='votes',
    title='Votos por Gênero',
    labels={'votes': 'Total de Votos', 'genre': 'Gênero'}
)
grafico_generos_votados.show()

# Criando o Dashboard
netflix_logo_url = "https://logodownload.org/wp-content/uploads/2014/10/netflix-logo-5.png"
stranger_things_image_url = "https://mcdn.wallpapersafari.com/medium/44/66/l5CPZ3.png"

#Ordenando os gêneros
generos_ordenados = sorted(df['genre'].unique())

#Removendo index
df = df.drop(columns=['lister-item-index'])

st.set_page_config(layout='wide')
st.title("Séries 📺")

aba1, aba2, aba3, aba4, aba5 = st.tabs(['Séries', 'Mais Avaliadas', 'Menos Avaliadas', 'Gênero', 'Recomendado'])

#Logo NetFlix
st.sidebar.image(netflix_logo_url, width=150)

traducao_colunas_dashboard = {
    'lister-item-index': 'Índice do Item',
    'lister-item-header': 'Nome da Série',
    'certificate': 'Classificação',
    'runtime': 'Duração',
    'genre': 'Gênero',
    'rating': 'Avaliação',
    'votes': 'Votos'
}

#Colunas Traduzidas
df_dashboard = df.rename(columns=traducao_colunas_dashboard)

#Filtro por gênero
with st.sidebar:
    st.sidebar.write("")
    generos_selecionados = st.sidebar.multiselect('Selecione os gêneros:', generos_ordenados)

#Definindo DataFrame baseado no filtro de gênero
if generos_selecionados:
    df_dashboard = df_dashboard[df_dashboard['Gênero'].str.lower().isin([genero.lower() for genero in generos_selecionados])]

# Definindo as abas do Dashboard
with aba1:
    st.dataframe(df_dashboard)

with aba2:
    st.plotly_chart(grafico_mais_avaliadas, use_container_width=True)

with aba3:
    st.plotly_chart(grafico_menos_avaliadas, use_container_width=True)

with aba4:
    st.plotly_chart(grafico_generos_votados, use_container_width=True)

with aba5:
    st.image(stranger_things_image_url, width=400)
    st.write("Stranger Things está no TOP 5 das séries mais bem avaliadas da Netflix. Uma série criada pelos irmãos Duffer onde um grupo de amigos se envolve em uma série de eventos sobrenaturais na pacata cidade de Hawkins. Eles enfrentam criaturas monstruosas, agências secretas do governo e se aventuram em dimensões paralelas.")

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido por: [Guilherme](https://www.linkedin.com/in/guilherme-wagner) e [Cristiano](https://www.linkedin.com/in/cristianolimamachado/) como trabalho acâdemico da matéria de Python.")
