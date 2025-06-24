import streamlit as st
from datetime import datetime
from modelo import analisar_imagem_carga, otimizar_imagem # IMPORTAMOS NOSSA FUNÇÃO DE IA

links_drive = {  
    "IMG-OK-1.png": "https://drive.google.com/uc?export=view&id=1ILelwalcJhR1C7uf54Aa7Z9rOf_ZT95_",  
    "IMG-OK-6.png": "https://drive.google.com/uc?export=view&id=1zsAx-tJ5ous8wtgWSMsQl7AfsRBhedVM",  
    "IMG-OK-8.png": "https://drive.google.com/uc?export=view&id=16hO3aunVOF_YAisYYmoOQhIOKXHjS_8a",  
    "IMG-OK-9.png": "https://drive.google.com/uc?export=view&id=1p4Brqn97IuSkWViCC6yJhLLnJbJ53vad",  
    "IMG-OK-10.png": "https://drive.google.com/uc?export=view&id=1o3lqG_M5uhHIr2HlB1mIU5wwoHRYNMNe",  
    "IMG-OK-11.png": "https://drive.google.com/uc?export=view&id=1A29s44IU5QIijVRTx5NXi0_rtGAjqTmX",  
    "n-okimg1.png": "https://drive.google.com/uc?export=view&id=1Sy36lY79PMI5mnJQD5DDilhPBGAfx0m-",  
    "n-okimg2.png": "https://drive.google.com/uc?export=view&id=1YTwNimCaKFCAR1agKGMEIPAERl3tHWoi",  
    "n-okimg3.png": "https://drive.google.com/uc?export=view&id=1hZiK6QmcSSkzz7tXRSBhJNntDvv3_gCI",  
    "n-okimg4.png": "https://drive.google.com/uc?export=view&id=1Rf7v2ivR_FoJcjdUIg-NFxHBkQgMQ-Lw",  
    "n-okimg5.png": "https://drive.google.com/uc?export=view&id=1JbUYFWFP2NO24jqu1bPN-TgIN-1nsMea",  
    "n-okimg6.png": "https://drive.google.com/uc?export=view&id=1IuomDwl6cp_UWQti2H-pkRYVi8o7mrSt"  
}

def render_page():
    """
    Renderiza a página 'Nova Carga' com formulário para upload de 3 fotos.
    """
    if st.button("‹ Voltar"):
        st.session_state.page = 'main'
        st.rerun()

    st.header("Nova Carga")

#Colocar algum texto falando sobre fazer uploud 
#    st.selectbox("Tipo de carga:", ["Selecione", "Pneus"], key="tipo_carga")
#    st.selectbox("Tipo de Base:", ["Selecione", "SP-MG"], key="tipo_base")
#    st.divider()

    st.subheader("Faça o upload de até 3 imagens da carga")
    
    # SIMPLIFICADO PARA 3 UPLOADS
    cols = st.columns(3)
    upload_labels = ["Foto 1", "Foto 2", "Foto 3"]
    for i, col in enumerate(cols):
        with col:
            with st.container(border=True):
                st.write(f"**{upload_labels[i]}**")
                uploaded_file = st.file_uploader(
                    label=f"uploader_{i}",
                    label_visibility="collapsed",
                    key=f"uploader_{i}",
                    type=['png', 'jpg', 'jpeg']
                )
                # Exibe a imagem se o arquivo foi carregado
                if uploaded_file is not None:
                    st.image(uploaded_file, caption=f"Pré-visualização {upload_labels[i]}", use_container_width=True)

    st.divider()

    if st.button("Enviar para análise", type="primary", use_container_width=True):
            # MOSTRA UM SPINNER ENQUANTO A IA TRABALHA
        with st.spinner("Analisando imagens... Isso pode levar um momento."):
            novo_id = 101 + len(st.session_state.cargas)
                
            uploaded_files_data = {}
            analises_ia = []
                
            # Loop pelos 3 uploaders
            for i in range(3):
                uploaded_file = st.session_state[f"uploader_{i}"]
                if uploaded_file is not None:
                    file_name = uploaded_file.name     
                    link = links_drive.get(file_name,None)  
                    #if link is not None:
                    #    resultado_analise = analisar_imagem_carga(link)   
                    #    print(resultado_analise)  
                    #    analises_ia.append(resultado_analise)
                    #else:                
                    image_bytes = uploaded_file.getvalue()
                    uploaded_files_data[i] = image_bytes
                    img_b64 = otimizar_imagem(image_bytes)

                        # CHAMA A FUNÇÃO DE ANÁLISE DA IA
                    resultado_analise = analisar_imagem_carga(img_b64)
                    analises_ia.append(resultado_analise)
                else:
                    analises_ia.append("Não enviada")

                # Cria o dicionário da nova carga com os resultados da IA
            nova_carga = {
                "id": novo_id,
                "data": datetime.now().strftime("%d/%m/%Y"),
            #    "tipo_carga": st.session_state.tipo_carga,
            #    "tipo_base": st.session_state.tipo_base,
                "percentage": 0,
                "uploaded_files": uploaded_files_data,
                "analises": analises_ia # SALVA OS RESULTADOS DA IA
            }
                
            st.session_state.cargas.append(nova_carga)

            st.success(f"Carga {novo_id} enviada e analisada com sucesso!")
            st.session_state.page = 'main'
            st.rerun()