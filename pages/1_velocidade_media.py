import pandas as pd
import streamlit as st
import plotly.express as px

# Inicio da configuração do dashboard no streamlit
st.set_page_config(page_title="Velocidade média", page_icon="logo.jpg", layout="wide")

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
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        background-color: #f8f9fb; 
        border: 1px solid #d3d3d3; 
        border-radius: 10px;       
        padding: 15px;             
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05); 
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def carregar_dados():
    # Leitura 
    df = pd.read_excel("velocidade_media_por_equip.xlsx")

    # Tratamento das colunas
    df["VELOCIDADE MEDIA"] = df["VELOCIDADE MEDIA"].str.replace('Km/h','')
    df["VELOCIDADE MEDIA"] = df["VELOCIDADE MEDIA"].astype(float)
    df["QUANTIDADE DE PASSAGENS"] = df["QUANTIDADE DE PASSAGENS"].astype(int)
    df[["CODIGO","LOCALIZACAO"]] = df["IDENTIFICAÇÃO"].str.split(' - ', n=1, expand=True)
    df = df.drop('IDENTIFICAÇÃO', axis=1)
    
    nova_ordem = ['CODIGO','LOCALIZACAO','QUANTIDADE DE PASSAGENS','VELOCIDADE MEDIA', 'Mês', 'Ano']
    df = df[nova_ordem]
    return df

df = carregar_dados()

# Mapeamento dos meses (Ideal fazer logo no começo)
meses_map = {
    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
    'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
    'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
}
df['Mes_Num'] = df['Mês'].str.lower().map(meses_map)

# ----------------- CABEÇALHO -----------------
st.markdown("<h1 style='text-align: center;'>Radares - Velocidade Média</h1>", unsafe_allow_html=True)
st.markdown("Este dashboard apresenta a análise de velocidade média registrada pelos radares de velocidade espalhados pela cidade. Os dado são retirados do sistema Sistrak.")
st.write("---") 

# ----------------- SIDEBAR E FILTROS -----------------
st.sidebar.image("logo_grande.png", use_container_width=True)
st.sidebar.header("Filtros")

# Filtro de Localização
loc_unica = df['LOCALIZACAO'].dropna().unique()
filtro_loc = st.sidebar.multiselect("Filtro por Localização", options=loc_unica, placeholder="Selecione...")

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
# APLICAÇÃO DOS FILTROS 
df_filtrado = df.copy()

if filtro_loc: 
    df_filtrado = df_filtrado[df_filtrado['LOCALIZACAO'].isin(filtro_loc)]
if filtro_ano:
    df_filtrado = df_filtrado[df_filtrado['Ano'].isin(filtro_ano)]
if filtro_mes:
    df_filtrado = df_filtrado[df_filtrado['Mês'].isin(filtro_mes)]

# ----------------- CÁLCULO DE MÉTRICAS (Usando dados filtrados) -----------------
if not df_filtrado.empty:
    # Usando .mean() que é a forma mais direta do Python calcular médias
    media_geral = df_filtrado["VELOCIDADE MEDIA"].mean()
    
    # Lógica do último mês baseada APENAS no que passou pelo filtro
    df_ordenado = df_filtrado.sort_values(by=['Ano', 'Mes_Num'], ascending=[False, False])
    ultimo_ano = df_ordenado['Ano'].iloc[0]
    ultimo_mes_nome = df_ordenado['Mês'].iloc[0].capitalize()
    texto_mes_ref = f"{ultimo_mes_nome}/{ultimo_ano}"
else:
    media_geral = 0
    texto_mes_ref = "Sem dados"

# ----------------- EXIBIÇÃO NO DASHBOARD -----------------
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Velocidade Média Geral", value=f"{media_geral:.2f} Km/h")

with col2:
    st.metric(label="Último Mês de Referência", value=texto_mes_ref)

#  gráfico
st.write("---")
st.markdown("<h2 style='text-align: center;'>Evolução da Velocidade Média em 2026</h2>", unsafe_allow_html=True)
df_grafico = df.copy()
if filtro_loc:
    df_grafico = df_grafico[df_grafico['LOCALIZACAO'].isin(filtro_loc)]
df_grafico = df_grafico[df_grafico['Ano'] == 2026]
df_agrupado = df_grafico.groupby(['Mes_Num', 'Mês'])['VELOCIDADE MEDIA'].mean().reset_index()
df_agrupado = df_agrupado.sort_values(by='Mes_Num')
fig = px.line(
    df_agrupado,
    x='Mês',
    y='VELOCIDADE MEDIA',
    markers=True, # Adiciona os pontos em cada mês
    text='VELOCIDADE MEDIA' # Mostra o valor em cima do ponto
    )
    
    # Formata os números para mostrar 2 casas decimais e o "km/h"
fig.update_traces(
    textposition="top center", 
    texttemplate='%{text:.2f} km/h',
    line=dict(width=3)
)
fig.update_layout(
        plot_bgcolor='rgb(245, 245, 255)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_range=[15,60]
    )
    
    # Exibe no Streamlit ocupando 100% da largura
st.plotly_chart(fig, use_container_width=True)

st.write("---") 
st.subheader("Tabela Detalhada de Radares")

# Limpando as colunas de data e a coluna auxiliar antes de exibir
df_exibicao = df_filtrado.drop(columns=['Mês', 'Ano', 'Mes_Num'], errors='ignore')
st.dataframe(df_exibicao)