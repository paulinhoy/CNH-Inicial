# modelo.py

import os 
from dotenv import load_dotenv 
from pathlib import Path
import base64 
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Carrega as variáveis de ambiente do arquivo .env na mesma pasta
dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path)
api_key = os.getenv("OPENAI_API_KEY")


# Inicializa o modelo de chat. 
# gpt-4o é uma excelente escolha por ser rápido e ter alta capacidade de visão.
llm = ChatOpenAI(
    model="gpt-4.1-mini-2025-04-14", 
    openai_api_key=api_key,
    max_tokens=10, # A resposta é muito curta ("Aprovado" ou "Reprovado")
    temperature=0, # Queremos a resposta mais direta e consistente possível
)

# Template do prompt, seguindo suas instruções
prompt_template = ChatPromptTemplate.from_messages([  
    ("system", "Você é um inspetor de cargas. Sua única tarefa é olhar para a imagem e responder 'Aprovado' se a carga parecer estar amarrada de forma segura, ou 'Reprovado' se não estiver ou se não for possível determinar. Não forneça nenhuma outra palavra ou explicação."
     "Para te auxiliar você irá receber junto com a pergunta exemplos de amarração que estão corretas e exemplos incorretos. Com base nos exemplos tome sua decisão"),  
    ("user", "{user_input}")  
])

# A chain que conecta o prompt ao modelo
chain = prompt_template | llm

imagem_teste = "https://drive.google.com/file/d/1jSrDquGm54-SVusx7FKENcC_A3tKcH0j/view?usp=sharing"

def analisar_imagem_carga(imagem_bytes: bytes) -> str:

    url_exemplo_conforme = "https://drive.google.com/uc?export=view&id=1oTQ0ZVLl09O5OlaLYScb9hrM5DiGundv"  
    url_exemplo_nao_conforme = "https://drive.google.com/uc?export=view&id=1x8QhdR6fqH7DuvQyuJak_0lg_kAo9txw"
    """
    Recebe os bytes de uma imagem, analisa se a carga está amarrada e retorna 'Aprovado' ou 'Reprovado'.
    Usa exemplos visuais de aprovação e reprovação como contexto.
    """
    if not api_key:
        return "API Key não configurada"

    try:
        # Codifica a imagem a ser analisada
        base64_image = base64.b64encode(imagem_bytes).decode('utf-8')

        # Prepara o input multimodal com exemplos e a imagem alvo
        input_multimodal = [
            {"type": "text", "text": "Exemplo de carga amarrada corretamente (Aprovado):"},
            {"type": "image_url", "image_url": {"url": f"{url_exemplo_conforme}"}},
            {"type": "text", "text": "Exemplo de carga amarrada de forma incorreta (Reprovado):"},
            {"type": "image_url", "image_url": {"url": f"{url_exemplo_nao_conforme}"}},
            {"type": "text", "text": "Agora, avalie a seguinte imagem:"},
        #    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            {"type": "text", "text": "A carga está amarrada de acordo com o exemplo aprovado ou reprovado? Responda apenas 'Aprovado' ou 'Reprovado'."}
        ]

        # Invoca a chain e obtém a resposta
        response = chain.invoke({"user_input": input_multimodal})

        # Limpa a resposta para garantir que temos apenas a palavra desejada
        resultado = response.content.strip()

        # Validação final para garantir que a resposta é o que esperamos
        if "aprovado" in resultado.lower():
            return "Aprovado"
        else:
            return "Reprovado"

    except Exception as e:
        print(f"Ocorreu um erro ao analisar a imagem: {e}")
        return "Erro na Análise"