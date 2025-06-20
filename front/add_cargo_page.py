# add_cargo_page.py

import streamlit as st
from datetime import datetime
from modelo import analisar_imagem_carga # IMPORTAMOS NOSSA FUNÇÃO DE IA

def render_page():
    """
    Renderiza a página 'Nova Carga' com formulário para upload de 3 fotos.
    """
    if st.button("‹ Voltar"):
        st.session_state.page = 'main'
        st.rerun()

    st.header("Nova Carga")

    st.selectbox("Tipo de carga:", ["Selecione", "Grãos", "Líquidos", "Refrigerados"], key="tipo_carga")
    st.selectbox("Tipo de Base:", ["Selecione", "Base SP", "Base RJ", "Base MG"], key="tipo_base")
    st.divider()

    st.subheader("Faça o upload de até 3 imagens da carga")
    
    # SIMPLIFICADO PARA 3 UPLOADS
    cols = st.columns(3)
    upload_labels = ["Foto 1", "Foto 2", "Foto 3"]
    for i, col in enumerate(cols):
        with col:
            with st.container(border=True):
                st.write(f"**{upload_labels[i]}**")
                st.file_uploader(
                    label=f"uploader_{i}",
                    label_visibility="collapsed",
                    key=f"uploader_{i}",
                    type=['png', 'jpg', 'jpeg']
                )

    st.divider()

    if st.button("Enviar para análise", type="primary", use_container_width=True):
        if st.session_state.tipo_carga == "Selecione" or st.session_state.tipo_base == "Selecione":
            st.warning("Por favor, selecione o tipo de carga e a base antes de enviar.")
        else:
            # MOSTRA UM SPINNER ENQUANTO A IA TRABALHA
            with st.spinner("Analisando imagens... Isso pode levar um momento."):
                novo_id = 101 + len(st.session_state.cargas)
                
                uploaded_files_data = {}
                analises_ia = []
                
                # Loop pelos 3 uploaders
                for i in range(3):
                    uploaded_file = st.session_state[f"uploader_{i}"]
                    if uploaded_file is not None:
                        image_bytes = uploaded_file.getvalue()
                        uploaded_files_data[i] = image_bytes
                        
                        # CHAMA A FUNÇÃO DE ANÁLISE DA IA
                        resultado_analise = analisar_imagem_carga(image_bytes)
                        print(resultado_analise)
                        analises_ia.append(resultado_analise)
                    else:
                        analises_ia.append("Não enviada")

                # Cria o dicionário da nova carga com os resultados da IA
                nova_carga = {
                    "id": novo_id,
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "tipo_carga": st.session_state.tipo_carga,
                    "tipo_base": st.session_state.tipo_base,
                    "percentage": 0,
                    "uploaded_files": uploaded_files_data,
                    "analises": analises_ia # SALVA OS RESULTADOS DA IA
                }
                
                st.session_state.cargas.append(nova_carga)

            st.success(f"Carga {novo_id} enviada e analisada com sucesso!")
            st.session_state.page = 'main'
            st.rerun()