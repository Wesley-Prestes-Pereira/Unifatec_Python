import streamlit as st

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

def formatar_tempo(dias):
    if dias >= 30:
        meses = dias // 30
        dias = dias % 30
        return f"{meses} mês(es)" + (f" e {dias} dia(s)" if dias > 0 else "")
    elif dias >= 7:
        semanas = dias // 7
        dias = dias % 7
        return f"{semanas} semana(s)" + (f" e {dias} dia(s)" if dias > 0 else "")
    else:
        return f"{dias} dia(s)"

def avancar_pagina():
    if st.session_state.pagina == 'tipo_website':
        st.session_state.pagina = 'tipo_linguagem'
    elif st.session_state.pagina == 'tipo_linguagem':
        st.session_state.pagina = 'funcionalidades'
    elif st.session_state.pagina == 'funcionalidades':
        if st.session_state.tipo_website == 'Landing Page':
            st.session_state.pagina = 'revisao'
        else:
            st.session_state.pagina = 'apis'
    elif st.session_state.pagina == 'apis':
        st.session_state.pagina = 'revisao'
    elif st.session_state.pagina == 'revisao':
        st.session_state.pagina = 'conclusao'

def retroceder_pagina():
    if st.session_state.pagina == 'tipo_linguagem':
        st.session_state.pagina = 'tipo_website'
    elif st.session_state.pagina == 'funcionalidades':
        st.session_state.pagina = 'tipo_linguagem'
    elif st.session_state.pagina == 'apis':
        st.session_state.pagina = 'funcionalidades'
    elif st.session_state.pagina == 'revisao':
        if st.session_state.tipo_website == 'Landing Page':
            st.session_state.pagina = 'funcionalidades'
        else:
            st.session_state.pagina = 'apis'
    elif st.session_state.pagina == 'conclusao':
        st.session_state.pagina = 'revisao'

# Inicialização do estado de sessão para armazenar preços e tempos atualizados
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'calculadora'
if 'nome' not in st.session_state:
    st.session_state.nome = ''
if 'email' not in st.session_state:
    st.session_state.email = ''
if 'tipo_website' not in st.session_state:
    st.session_state.tipo_website = ''
if 'tipo_linguagem' not in st.session_state:
    st.session_state.tipo_linguagem = ''
if 'funcionalidades_selecionadas' not in st.session_state:
    st.session_state.funcionalidades_selecionadas = []
if 'apis_selecionadas' not in st.session_state:
    st.session_state.apis_selecionadas = []
if 'projeto_concluido' not in st.session_state:
    st.session_state.projeto_concluido = False

if 'precos_funcionalidades' not in st.session_state or 'precos_apis' not in st.session_state:
    st.session_state['precos_funcionalidades'] = {
        "Landing Page": [
            {"funcionalidade": "Formulário de contato", "preco": 300, "tempo": 3},
            {"funcionalidade": "Botões para chamar atenção", "preco": 200, "tempo": 2},
            {"funcionalidade": "Links para redes sociais", "preco": 150, "tempo": 1}
        ],
        "Hotsite": [
            {"funcionalidade": "Contagem regressiva para o evento", "preco": 400, "tempo": 5},
            {"funcionalidade": "Galeria de imagens e vídeos", "preco": 500, "tempo": 7},
            {"funcionalidade": "Formulário de inscrição ou participação", "preco": 300, "tempo": 4}
        ],
        "Institucional": [
            {"funcionalidade": "Blog ou notícias", "preco": 600, "tempo": 10},
            {"funcionalidade": "Formulário de contato", "preco": 300, "tempo": 3},
            {"funcionalidade": "Mapa com a localização da empresa", "preco": 250, "tempo": 2},
            {"funcionalidade": "Links para redes sociais", "preco": 150, "tempo": 1}
        ],
        "Loja Virtual": [
            {"funcionalidade": "Filtro de produtos", "preco": 500, "tempo": 5},
            {"funcionalidade": "Seção para avaliações e comentários dos clientes", "preco": 400, "tempo": 4},
            {"funcionalidade": "Controle financeiro", "preco": 700, "tempo": 14},
            {"funcionalidade": "Chat ou chatbot para atendimento", "preco": 600, "tempo": 10},
            {"funcionalidade": "Barra de pesquisa interna", "preco": 300, "tempo": 3},
            {"funcionalidade": "Funcionalidades específicas", "preco": 800, "tempo": 20}
        ]
    }
    st.session_state['precos_apis'] = [
        {"api": "API de Frete", "preco": 800, "tempo": 5},
        {"api": "API de Pagamento", "preco": 1000, "tempo": 7},
        {"api": "API de Estoque", "preco": 900, "tempo": 6},
        {"api": "API de Comparação de Preços", "preco": 850, "tempo": 5},
        {"api": "API de Personalização", "preco": 950, "tempo": 6}
    ]

# Menu lateral para navegação
st.sidebar.title("Menu de navegação")
if st.sidebar.button("Tabela de preços"):
    st.session_state.pagina = 'preços'
if st.sidebar.button("Calculadora"):
    st.session_state.pagina = 'calculadora'

# Tabela de preços
if st.session_state.get('pagina') == 'preços':
    st.title("Tabelas de preços de serviços")
    col_funcionalidades, col_apis = st.columns(2)
    with col_funcionalidades:
        st.subheader("Funcionalidades")
        for tipo, funcionalidades in st.session_state.precos_funcionalidades.items():
            st.subheader(f"{tipo}")
            for func in funcionalidades:
                new_price = st.number_input(f"{func['funcionalidade']}", value=func["preco"], key=f"new_price_{tipo}_{func['funcionalidade']}")
                if new_price != func["preco"]:
                    func["preco"] = new_price
                    st.session_state.precos_funcionalidades[tipo] = funcionalidades.copy()

    with col_apis:
        st.subheader("APIs")
        for api in st.session_state.precos_apis:
            new_price = st.number_input(f"{api['api']}", value=api["preco"], key=f"new_price_api_{api['api']}")
            if new_price != api["preco"]:
                api["preco"] = new_price
                # Atualizar o estado global após alteração
                st.session_state.precos_apis = [api.copy() for api in st.session_state.precos_apis]

# Calculadora de Projetos

if st.session_state.get('pagina') == 'calculadora':
    st.title("Seja bem-vindo(a)")
    st.write("Bem-vindo(a) ao nosso modelo de calculadora de projetos! Com ele, você pode estimar o custo para desenvolver seu próprio website. Nossos websites possuem um layout responsivo que se adapta a smartphones, tablets, notebooks e desktops, além de contar com um design moderno e atraente. Preencha os campos abaixo para continuar.")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.nome = st.text_input("Digite seu nome:")
    with col2:
        st.session_state.email = st.text_input("E-mail para entrarmos contato:")
    if st.session_state.nome and st.session_state.email:
        if st.button("Próximo"):
            st.session_state.pagina = 'tipo_website'
elif st.session_state.pagina == 'tipo_website':
    st.title("Calculadora de Projetos")
    st.subheader("Escolha o tipo de Website")
    tipo_website = st.selectbox("Tipo de Website", ["", "Landing Page", "Hotsite", "Institucional", "Loja Virtual"])
    if tipo_website:
      if st.button("Próximo"):
          st.session_state.tipo_website = tipo_website
          avancar_pagina()

elif st.session_state.pagina == 'tipo_linguagem':
    st.title("Calculadora de Projetos")
    st.subheader("Escolha a linguagem")
    tipo_linguagem = st.selectbox("Linguagem", ["", "WordPress", "Personalizado"], index=st.session_state.tipo_linguagem_index if 'tipo_linguagem_index' in st.session_state else 0)
    if tipo_linguagem:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Anterior"):
                retroceder_pagina()
        with col2:
            if st.button("Próximo"):
                st.session_state.tipo_linguagem = tipo_linguagem
                avancar_pagina()

elif st.session_state.pagina == 'funcionalidades':
    st.title("Calculadora de Projetos")
    st.subheader(f"Funcionalidades de {st.session_state.tipo_website}")
    funcionalidades = st.session_state.precos_funcionalidades[st.session_state.tipo_website]
    with st.form(key='funcionalidades_form'):
        temp_funcionalidades_selecionadas = [
            func for func in funcionalidades
            if st.checkbox(func['funcionalidade'], key=f"check_{st.session_state.tipo_website}_{func['funcionalidade']}")
        ]
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Anterior"):
                retroceder_pagina()
        with col2:
            if st.form_submit_button("Próximo"):
                st.session_state.funcionalidades_selecionadas = temp_funcionalidades_selecionadas
                avancar_pagina()

elif st.session_state.pagina == 'apis':
    st.title("Calculadora de Projetos")
    st.subheader("APIs")
    with st.form(key='apis_form'):
        temp_apis_selecionadas = [
            api for api in st.session_state.precos_apis if st.checkbox(api['api'], key=f"check_api_{api['api']}")
        ]
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Anterior"):
                retroceder_pagina()
        with col2:
            if st.form_submit_button("Revisão"):
                st.session_state.apis_selecionadas = temp_apis_selecionadas
                avancar_pagina()

elif st.session_state.pagina == 'revisao':
    st.title("Calculadora de Projetos")
    st.subheader("Resumo do Projeto")
    total_funcionalidades = sum(func["preco"] for func in st.session_state.funcionalidades_selecionadas)
    tempo_funcionalidades = sum(func["tempo"] for func in st.session_state.funcionalidades_selecionadas)
    total_apis = sum(api["preco"] for api in st.session_state.apis_selecionadas)
    tempo_apis = sum(api["tempo"] for api in st.session_state.apis_selecionadas)
    total_geral = total_funcionalidades + total_apis
    tempo_total = tempo_funcionalidades + tempo_apis
    if st.session_state.tipo_linguagem == "Personalizado":
        total_funcionalidades *= 2
        total_apis *= 2
        tempo_funcionalidades *= 2
        tempo_apis *= 2
        total_geral = total_funcionalidades + total_apis
        tempo_total = tempo_funcionalidades + tempo_apis
    st.markdown(f"**Total de Funcionalidades:** <span style='color:rgb(255 85 85);'>{formatar_moeda(total_funcionalidades)}</span>", unsafe_allow_html=True)
    st.markdown(f"**Tempo estimado para funcionalidades:** <span style='color:rgb(255 85 85);'>{formatar_tempo(tempo_funcionalidades)}</span>", unsafe_allow_html=True)
    st.markdown(f"**Total de APIs:** <span style='color:rgb(255 85 85);'>{formatar_moeda(total_apis)}</span>", unsafe_allow_html=True)
    st.markdown(f"**Tempo estimado para APIs:** <span style='color:rgb(255 85 85);'>{formatar_tempo(tempo_apis)}</span>", unsafe_allow_html=True)
    st.markdown(f"**Total Geral:** <span style='color:rgb(255 85 85);'>{formatar_moeda(total_geral)}</span>", unsafe_allow_html=True)
    st.markdown(f"**Tempo estimado total:** <span style='color:rgb(255 85 85);'>{formatar_tempo(tempo_total)}</span>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Anterior"):
            retroceder_pagina()
    with col2:
        if st.button("Concluir"):
            st.session_state.projeto_concluido = True
            avancar_pagina()

elif st.session_state.pagina == 'conclusao' and st.session_state.projeto_concluido:
    st.title("Calculadora de Projetos")
    total_funcionalidades = sum(func["preco"] for func in st.session_state.funcionalidades_selecionadas)
    tempo_funcionalidades = sum(func["tempo"] for func in st.session_state.funcionalidades_selecionadas)
    total_apis = sum(api["preco"] for api in st.session_state.apis_selecionadas)
    tempo_apis = sum(api["tempo"] for api in st.session_state.apis_selecionadas)
    if st.session_state.tipo_linguagem == "Personalizado":
        total_funcionalidades *= 2
        total_apis *= 2
        tempo_funcionalidades *= 2
        tempo_apis *= 2
    total_geral = total_funcionalidades + total_apis
    tempo_total = tempo_funcionalidades + tempo_apis
    st.write("Obrigado por entrar em contato " + st.session_state.nome + ", vamos analisar seu projeto e entrar em contato posteriormente pelo e-mail: " + st.session_state.email)
    st.subheader("Detalhes do seu projeto:")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Valor total do projeto:")
        st.markdown(f"**Total Geral:** <span style='color:rgb(255 85 85);'>{formatar_moeda(total_geral)}</span>", unsafe_allow_html=True)
        st.markdown(f"**Tempo estimado total:** <span style='color:rgb(255 85 85);'>{formatar_tempo(tempo_total)}</span>", unsafe_allow_html=True)
    with col2:
        st.subheader("Detalhes do projeto:")
        for func in st.session_state.funcionalidades_selecionadas:
            preco_display = func["preco"] * 2 if st.session_state.tipo_linguagem == "Personalizado" else func["preco"]
            tempo_display = func["tempo"] * 2 if st.session_state.tipo_linguagem == "Personalizado" else func["tempo"]
            st.markdown(f"{func['funcionalidade']} - Valor: <span style='color:rgb(255 85 85);'>{formatar_moeda(preco_display)}</span> e Tempo: <span style='color:rgb(255 85 85);'>{formatar_tempo(tempo_display)}</span>", unsafe_allow_html=True)
        for api in st.session_state.apis_selecionadas:
            preco_display = api["preco"] * 2 if st.session_state.tipo_linguagem == "Personalizado" else api["preco"]
            tempo_display = api["tempo"] * 2 if st.session_state.tipo_linguagem == "Personalizado" else api["tempo"]
            st.markdown(f"{api['api']} - Valor: <span style='color:rgb(255 85 85);'>{formatar_moeda(preco_display)}</span> e Tempo: <span style='color:rgb(255 85 85);'>{formatar_tempo(tempo_display)}</span>", unsafe_allow_html=True)
