import streamlit as st
from streamlit_option_menu import option_menu

# Configure a página
st.set_page_config(layout='wide')

# Importe suas páginas
from kpi import show as show_kpi
from calendario import show as show_calendario
from grafico import show as show_grafico

# Inicialize o estado da sessão
if 'page' not in st.session_state:
    st.session_state.page = ''

# Crie um menu de opções para cada página
with st.sidebar:
    st.session_state.page = option_menu("Menu Principal", ['KPI', 'Calendário', 'Gráfico'], 
        icons=['bar-chart', 'calendar', 'chart-line'], menu_icon="list", default_index=0)

# Exiba a página selecionada
if st.session_state.page == 'KPI':
    show_kpi()
elif st.session_state.page == 'Calendário':
    show_calendario()
elif st.session_state.page == 'Gráfico':
    show_grafico()
