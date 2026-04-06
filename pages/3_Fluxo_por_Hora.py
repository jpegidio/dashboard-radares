import pandas as pd
import streamlit as st
import plotly.express as px
import calendar

st.set_page_config(page_title="Fluxo por Hora", page_icon="logo.jpg", layout="wide")
st.sidebar.image("logo_grande.png", use_container_width=True)
st.markdown("<h1 style='text-align: center;'>Radares - Fluxo por Hora</h1>", unsafe_allow_html=True)
st.markdown("Este dashboard apresenta a contagem de veículos por hora registradas pelos radares de velocidade espalhados pela cidade. Os dado são retirados do sistema Sistrak.")
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
    div[data-testid="stSelectbox"] label p {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def carregar_dados():
    df = pd.read_excel("fluxo_por_hora.xlsx")
    
    colunas_horas = [f"{i}h" for i in range(24)]
    for col in colunas_horas:
        df[col] = df[col].replace(['-', ' - '], 0).astype(int)
        
    df["TOTAL"] = df["TOTAL"].replace(['-', ' - '], 0).astype(int)
    
    meses_map = {
    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
    'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
    'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    df['Mes_Num'] = df['Mês'].str.lower().map(meses_map)
    df['Dias_no_Mes'] = df.apply(lambda linha: calendar.monthrange(linha['Ano'], linha['Mes_Num'])[1], axis=1)

    return df

df = carregar_dados()

loc_unica = df['ENDEREÇO'].dropna().unique()
filtro_loc = st.sidebar.multiselect("Filtro por Localização", options=loc_unica, placeholder="Selecione...")

df_filtrado = df.copy()

if filtro_loc:
    df_filtrado = df_filtrado[df_filtrado['ENDEREÇO'].isin(filtro_loc)]

colunas_horas = [f"{i}h" for i in range(24)]

if not df_filtrado.empty:
    df_agrupado = df_filtrado.groupby('ENDEREÇO')[colunas_horas + ['Dias_no_Mes']].sum()
    vmd_por_radar = df_agrupado[colunas_horas].div(df_agrupado['Dias_no_Mes'], axis=0)
    
    media_diaria_horas = vmd_por_radar.sum().reset_index()
    media_diaria_horas.columns = ['Hora', 'Volume Médio Diário']
    media_diaria_horas['Volume Médio Diário'] = media_diaria_horas['Volume Médio Diário'].round(0).fillna(0).astype(int)
else:
    media_diaria_horas = pd.DataFrame({'Hora': colunas_horas, 'Volume Médio Diário': 0})

st.markdown("<h2 style='text-align: center;'>Distribuição do Fluxo ao Longo do Dia</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Média por Hora</h2>", unsafe_allow_html=True)

fig = px.bar(
    media_diaria_horas,
    x='Hora',
    y='Volume Médio Diário',
    text_auto=True 
)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Horário do Dia",
    yaxis_title="Volume Médio Diário de Veículos"
)

st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.subheader("Tabela Detalhada")

# Remove as colunas auxiliares apenas na hora de exibir a tabela para o usuário
df_exibicao = df_filtrado.drop(columns=['Mes_Num', 'Dias_no_Mes'], errors='ignore')
st.dataframe(df_exibicao)