import pandas as pd
import streamlit as st

st.set_page_config(page_title="Contagem por Classificação", page_icon="logo.jpg", layout="wide")
st.sidebar.image("logo_grande.png", use_container_width=True)
st.markdown("<h1 style='text-align: center;'>Radares - Contagem por Classificação</h1>", unsafe_allow_html=True)
st.markdown("Este dashboard apresenta a contagem de veículos separados por classificação registradas pelos radares de velocidade espalhados pela cidade. Os dado são retirados do sistema Sistrak.")
st.write("---") 

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        color: #ffffff;
    }
    [data-testid="stSidebarNav"] span {
        color: #ffffff !important;
    }
    [data-testid="stMetric"] {
        /* Centralização */
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        
        /* O "Card" */
        background-color: #f8f9fb; /* Um cinza bem clarinho de fundo */
        border: 1px solid #d3d3d3; /* A bordinha cinza */
        border-radius: 10px;       /* Cantos arredondados */
        padding: 15px;             /* Espaço entre o texto e a borda */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05); /* Sombra leve */
    }
    div[data-testid="stSelectbox"] label p {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def carregar_dados():
    # Leitura 
    df = pd.read_excel("contagem_classificacao.xlsx")
    # Tratamento das colunas
    df = df.drop('TIPO', axis=1)
    df["Moto"] = df["Moto"].replace(' - ', 0).astype(int)
    df["Automóvel"] = df["Automóvel"].replace(' - ', 0).astype(int)
    df["Caminhão"] = df["Caminhão"].replace(' - ', 0).astype(int)
    df["Ônibus"] = df["Ônibus"].replace(' - ', 0).astype(int)
    df["TOTAL"] = df["TOTAL"].replace(' - ', 0).astype(int)
    meses_map = {
    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
    'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
    'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    df['Mes_Num'] = df['Mês'].str.lower().map(meses_map)

    return df

df=carregar_dados()

st.sidebar.header("Filtros")

# Filtro por Localização
loc_unica = df['ENDEREÇO'].dropna().unique()
filtro_loc = st.sidebar.multiselect(
    "Filtro por Localização",
    options=loc_unica,
    placeholder="Selecione..."
)
if filtro_loc: 
    df = df[df['ENDEREÇO'].isin(filtro_loc)]

id_unico = df['IDENTIFICAÇÃO'].dropna().unique()
filtro_id = st.sidebar.multiselect(
    "Filtro por Equipamento",
    options=id_unico,
    placeholder="Selecione..."
)
if filtro_id: 
    df = df[df['IDENTIFICAÇÃO'].isin(filtro_id)]

df_ordenado_geral = df.sort_values(by=['Ano', 'Mes_Num'], ascending=[False, False])
ultimo_mes_disponivel = df_ordenado_geral['Mês'].iloc[0]
ultimo_ano_disponivel = df_ordenado_geral['Ano'].iloc[0]

# Filtro de Ano
ano_unico = df['Ano'].dropna().unique()
filtro_ano = st.sidebar.multiselect(
    "Filtro por Ano",
    options=ano_unico, 
    default=[ultimo_ano_disponivel],
    placeholder="Selecione...")

# 2. Filtro de Mês
mes_unico = df['Mês'].dropna().unique()
filtro_mes = st.sidebar.multiselect(
    "Filtro por Mês", 
    options=mes_unico, 
    default=[ultimo_mes_disponivel],
    placeholder="Selecione..."
)

soma_total = df["TOTAL"].sum()

pct_carro = f"{df['Automóvel'].sum() / df['TOTAL'].sum():.2%}"
pct_moto = f"{df['Moto'].sum() / df['TOTAL'].sum():.2%}"
pct_truck = f"{df['Caminhão'].sum() / df['TOTAL'].sum():.2%}"
pct_bus = f"{df['Ônibus'].sum() / df['TOTAL'].sum():.2%}"

st.markdown("<h2 style='text-align: center;'>Composição do tráfego</h1>", unsafe_allow_html=True)
st.markdown("Porcentagem da composição do tráfego na cidade. Cálculo baseado na contagem e classificação dos radares.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Automóveis", value=pct_carro)
with col2:
    st.metric(label="Motos", value=pct_moto)
with col3:
    st.metric(label="Caminhões", value=pct_truck)
with col4:
    st.metric(label="Ônibus", value=pct_bus)
st.write("---") 

st.markdown("<h2 style='text-align: center;'>Tabela detalhada</h2>", unsafe_allow_html=True)

st.dataframe(df)