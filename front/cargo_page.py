# cargo_page.py
import streamlit as st
from modelo import analisar_imagem_carga, otimizar_imagem

def render_page(modo_edicao=True):
    """
    Renderiza a página de detalhes e/ou edição de uma carga existente.
    Se modo_edicao=False, os campos ficam desabilitados e não aparece botão de salvar.
    """
    selected_id = st.session_state.get('selected_cargo_id')
    if not selected_id:
        st.error("Nenhuma carga selecionada.")
        if st.button("Voltar para a lista"):
            st.session_state.page = 'main'
            st.rerun()
        return

    carga_selecionada = next((carga for carga in st.session_state.cargas if carga['id'] == selected_id), None)

    if carga_selecionada is None:
        st.error(f"Carga com ID {selected_id} não encontrada.")
        if st.button("Voltar para a lista"):
            st.session_state.page = 'main'
            st.rerun()
        return

    if st.button("‹ Voltar"):
        st.session_state.page = 'main'
        st.rerun()

    st.header(f"Carga {carga_selecionada['id']}")

    tipos_carga = ["Selecione", "Pneus"]
    tipos_base = ["Selecione", "SP-MG"]
    index_carga = tipos_carga.index(carga_selecionada.get('tipo_carga', 'Selecione'))
    index_base = tipos_base.index(carga_selecionada.get('tipo_base', 'Selecione'))

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Tipo de carga:", tipos_carga, index=index_carga, key="edit_tipo_carga", disabled=not modo_edicao)
    with col2:
        st.selectbox("Tipo de Base:", tipos_base, index=index_base, key="edit_tipo_base", disabled=not modo_edicao)

    st.divider()

    tab_fotos, tab_video = st.tabs(["Fotos", "Vídeo"])

    # --- Apenas 3 campos de upload ---
    upload_labels = [
        "Foto 1", "Foto 2", "Foto 3"
    ]

    existing_files = carga_selecionada.get('uploaded_files', {})

    with tab_fotos:
        st.subheader("Imagens da carga")
        cols = st.columns(len(upload_labels))
        for i, label in enumerate(upload_labels):
            with cols[i]:
                st.write(f"**{label}**")
                if i in existing_files:
                    st.image(existing_files[i], use_container_width=True, caption="Imagem atual")
                else:
                    st.caption("Nenhuma imagem enviada.")
                if modo_edicao:
                    st.file_uploader(
                        label=f"edit_uploader_{i}",
                        label_visibility="collapsed",
                        key=f"edit_uploader_{i}",
                        type=['png', 'jpg', 'jpeg']
                    )
                    # Exibe a imagem se um novo arquivo foi carregado
                    if st.session_state.get(f"edit_uploader_{i}") is not None:
                        st.image(st.session_state[f"edit_uploader_{i}"], caption="Nova imagem", use_container_width=True)

    with tab_video:
        st.info("A funcionalidade de upload de vídeo será implementada em breve.")

    st.divider()

    # Exibe o resultado da IA, se disponível
    if "analises" in carga_selecionada and carga_selecionada["analises"]:
        st.subheader("Resultado da IA:")
        for idx, resultado in enumerate(carga_selecionada["analises"], 1):
            st.write(f"{idx}° Foto: {resultado.lower()}")
    else:
        st.info("Nenhum resultado de IA disponível para esta carga.")

    # --- Botão de salvar só aparece no modo edição ---
    if modo_edicao:
        if st.button("Atualizar Análise", type="primary", use_container_width=True):
            index_to_update = next((i for i, carga in enumerate(st.session_state.cargas) if carga['id'] == selected_id), None)
            if index_to_update is not None:
                carga = st.session_state.cargas[index_to_update]
                tipos_carga = st.session_state.edit_tipo_carga
                tipos_base = st.session_state.edit_tipo_base

                with st.spinner("Analisando imagens... Isso pode levar um momento."):
                    uploaded_files_data = {}
                    analises_ia = []
                    for i in range(len(upload_labels)):
                        uploaded_file = st.session_state.get(f"edit_uploader_{i}")
                        imagem_antiga = carga.get("uploaded_files", {}).get(i)
                        resultado_antigo = carga.get("analises", [])[i] if "analises" in carga and len(carga["analises"]) > i else "Não enviada"
                        if uploaded_file is not None:
                            image_bytes = uploaded_file.getvalue()
                            if (imagem_antiga is None) or (imagem_antiga != image_bytes):
                                img_b64 = otimizar_imagem(image_bytes)
                                resultado_analise = analisar_imagem_carga(img_b64)
                                analises_ia.append(resultado_analise)
                            else:
                                analises_ia.append(resultado_antigo)
                            uploaded_files_data[i] = image_bytes
                        else:
                            if imagem_antiga is not None:
                                uploaded_files_data[i] = imagem_antiga
                                analises_ia.append(resultado_antigo)
                            else:
                                analises_ia.append("Não enviada")

                carga["tipo_carga"] = tipos_carga
                carga["tipo_base"] = tipos_base
                carga["uploaded_files"] = uploaded_files_data
                carga["analises"] = analises_ia
                carga["percentage"] = 0  # Exemplo

                st.success(f"Carga {selected_id} atualizada e analisada com sucesso!")
                st.session_state.page = 'main'
                st.rerun()