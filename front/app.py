import streamlit as st
from datetime import datetime
import add_cargo_page
import cargo_page  # Novo arquivo unificado para detalhes/edição

# --- Configuração da página e CSS ---
st.set_page_config(layout="wide")
st.markdown("""
<style>
    .main-header { font-size: 24px; font-weight: bold; margin-bottom: 20px; }
    .card { border: 1px solid #e0e0e0; border-radius: 5px; padding: 15px; margin-bottom: 10px; background-color: white; }
    .percentage { border-radius: 50%; width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; }
    .percentage-green { background-color: #e6f7e6; color: #2e8b57; }
    .percentage-yellow { background-color: #fff8e6; color: #ffa500; }
    .percentage-gray { background-color: #f0f0f0; color: #808080; }
    .search-container { display: flex; margin-bottom: 20px; }
    .add-button { background-color: #20b2aa; color: white; border: none; border-radius: 5px; padding: 8px 16px; cursor: pointer; font-weight: bold; }
    .date-info { color: #666; font-size: 14px; display: flex; align-items: center; }
    .date-icon { margin-right: 5px; }
    .cargo-title { color: #0074D9; font-weight: bold; }
    .sidebar .sidebar-content { background-color: #1e2e2e; color: white; }
    .cnh-logo { background-color: #BABABA; border-radius: 10px; padding: 10px; margin-bottom: 20px; text-align: center; font-weight: bold; font-size: 24px; }
    .sidebar-menu-item { display: flex; align-items: center; padding: 10px 0; color: #20b2aa; text-decoration: none; margin-bottom: 5px; font-size: 18px; font-weight: bold; border-radius: 5px; transition: background 0.2s; }
    .sidebar-menu-item:hover { background-color: rgba(255, 255, 255, 0.1); }
    .sidebar-menu-icon { margin-right: 10px; }
    .welcome-text { color: black; font-size: 14px; margin-bottom: 5px; }
    .user-name { color: black; font-size: 20px; font-weight: bold; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- Estado da aplicação ---
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'cargas' not in st.session_state:
    st.session_state.cargas = []
if 'selected_cargo_id' not in st.session_state:
    st.session_state.selected_cargo_id = None

def change_page(page_name, cargo_id=None):
    st.session_state.page = page_name
    st.session_state.selected_cargo_id = cargo_id

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="cnh-logo">CNH</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-text">Bem-vindo,</div>', unsafe_allow_html=True)
    st.markdown('<div class="user-name">User</div>', unsafe_allow_html=True)
    if st.button("Conferência de Cargas", use_container_width=True):
        change_page('main')
    if st.button("Dashboards", use_container_width=True):
        st.info("Página de Dashboards em construção!")

# --- Página principal ---
def render_main_page():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown('<div class="main-header">Conferência de cargas</div>', unsafe_allow_html=True)
    with col2:
        if st.button("+ Adicionar Carga", type="primary", on_click=change_page, args=('add_cargo',)):
            pass
    st.text_input("Pesquisar", placeholder="Pesquisar por ID da carga...", key="search", label_visibility="collapsed")
    st.divider()

    if not st.session_state.cargas:
        st.info("Nenhuma carga para exibir no momento. Adicione uma nova carga para começar.")
    else:
        num_cols = 4
        cargas_para_exibir = reversed(st.session_state.cargas)
        for i, carga in enumerate(cargas_para_exibir):
            if i % num_cols == 0:
                cols = st.columns(num_cols)
            with cols[i % num_cols]:
                with st.container(border=True):
                    if carga['percentage'] >= 90: percentage_class = "percentage-green"
                    elif carga['percentage'] >= 70: percentage_class = "percentage-yellow"
                    else: percentage_class = "percentage-gray"
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <div class="cargo-title">Carga {carga['id']}</div>
                            <div class="date-info">
                                <span class="date-icon">📅</span> {carga['data']}
                            </div>
                        </div>
                        <div class="percentage {percentage_class}">{carga['percentage']}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                    # Botão para ver detalhes (modo só leitura)
                    if st.button("Ver Detalhes", key=f"details_{carga['id']}", use_container_width=True):
                        change_page('details_cargo', cargo_id=carga['id'])
                        st.rerun()
                    # Botão para editar
                    if st.button("Editar", key=f"edit_{carga['id']}", use_container_width=True):
                        change_page('edit_cargo', cargo_id=carga['id'])
                        st.rerun()

# --- Roteador Principal ---
if st.session_state.page == 'main':
    render_main_page()
elif st.session_state.page == 'add_cargo':
    add_cargo_page.render_page()
elif st.session_state.page == 'edit_cargo':
    cargo_page.render_page(modo_edicao=True)
elif st.session_state.page == 'details_cargo':
    cargo_page.render_page(modo_edicao=False)