import streamlit as st

st.set_page_config(page_title="Relatório - Radares", page_icon="logo.jpg", layout="wide")
st.sidebar.image("logo_grande.png", use_container_width=True)

import streamlit as st

import streamlit as st

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        color: #ffffff;
    }
    [data-testid="stSidebarNav"] span {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Título da sua Home Page
st.title("Dashboard de Radares de Velocidade- Joinville")
st.markdown("Os dados presentes nesses relatórios são extraídos do sistema Sistrak. Selecione abaixo qual relatório você deseja visualizar:")

col1, col2, col3 = st.columns(3)

with col1:
    # O estilo CSS abaixo aumenta a altura dos botões apenas nesta página
    st.markdown("""
    <style>
    /* 1. Ajusta o texto que já existe dentro do botão */
    div.stButton > button p {
        font-size: 30px !important;
        font-weight: bold;
        margin: 0px !important;
        line-height: 1.2 !important;
    }

    /* 2. Adiciona o texto novo apenas UMA vez no final do botão */
    div.stButton > button::after {
        content: 'Por Equipamento'; 
        display: block;
        font-size: 16px !important;
        font-weight: normal;
        color: #666;
        margin-top: 10px;
        text-align: center;
        width: 100%;
    }

    /* 3. Ajusta a altura e centralização do conteúdo */
    div.stButton > button {
        height: 200px; 
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("🏎 \n\n Velocidade Média", use_container_width=True):
        st.switch_page("pages/1_velocidade_media.py")
