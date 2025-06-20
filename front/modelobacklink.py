import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import re

# Carrega a chave da API do .env
dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path)
api_key = os.getenv("OPENAI_API_KEY")

def link_drive_direto(link: str) -> str:
    """
    Recebe um link de compartilhamento do Google Drive e retorna o link direto para a imagem.
    """
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', link)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    else:
        return link  # Se não for do Google Drive, retorna o link original

def analisar_imagem_carga(image_url):
    prompt = """  
Você é um inspetor de cargas responsável por avaliar a amarração de pneus em caminhões a partir de imagens.

Siga as instruções abaixo para avaliar se a carga está amarrada corretamente:

Critérios de avaliação:
- As cintas de amarração devem estar presas nos pontos de ancoragem externos e visíveis da carroceria.
- Olhais ou ganchos atendem as especificações. Ganchos podem ser presos em pontos da carroceria que estejam visiveis como mostrado no exemplo conforme.
- Não é permitido que as cintas passem para uma parte interna da carroceria como mostrado no exemplo não conforme.
- Não é permitida a passagem de correntes ou cordas pelo ponto de amarração na carroceria.

**Orientação adicional:**  
Se a cinta estiver claramente presa em um ponto de ancoragem externo, considere como conforme, mesmo que o gancho não esteja totalmente visível na imagem. Descreva o ponto de fixação observado.

Exemplo de amarração incorreta: (exemplo não conforme)  
A cinta de amarração presa diretamente em um furo da estrutura do caminhão, sem nenhum acessório adicional visível.

Exemplo de amarração correta (exemplo conforme)
a cinta presa a um gancho metálico (tipo olhal ou argola) que está fixado na estrutura do caminhão. Ou seja, há um acessório intermediário entre a cinta e a carroceria.

Com base nesses critérios, avalie a imagem fornecida e responda:
- A carga está amarrada corretamente?
- Se houver irregularidades, explique quais são e por que podem ser prejudiciais.

FORMATO DA RESPOSTA:
1. AVALIAÇÃO: [CONFORME/NÃO CONFORME]
2. GANCHOS IDENTIFICADOS: [SIM/NÃO/PARCIALMENTE VISÍVEL] - descreva o ponto de fixação observado
3. IRREGULARIDADES: [listar se houver]
4. JUSTIFICATIVA: [explicação técnica baseada nos critérios]

*IMPORTANTE* Responda com base apenas nos critérios fornecidos. Não avalie situações que não estão escritas explicitamente nos critérios de avaliação.
Responda em português, de forma clara e objetiva.
"""

    llm = ChatOpenAI(
        api_key=api_key,
        model="gpt-4o",
        temperature=0.2,
        max_tokens=256,
    )
    
    #Imagem usada de exemplo
    image_exemplo_naoconforme = "https://drive.google.com/uc?export=view&id=1Q0l-6NBVyfBgAqT6zgRb9Lx8PPT_9Njd"
    image_exemplo_conforme = "https://drive.google.com/uc?export=view&id=1OksBl8pXCKt9Khnzluz8feXt69rITAsT"

    messages = [
        SystemMessage(content="Você é um assistente que descreve imagens de forma detalhada."),
        HumanMessage(
            content=[
                {"type": "text", "text": "Exemplo não conforme:"},
                {"type": "image_url", "image_url": {"url": image_exemplo_naoconforme}},
                {"type": "text", "text": "Exemplo conforme:"},
                {"type": "image_url", "image_url": {"url": image_exemplo_conforme}},
                {"type": "text", "text": f"{prompt}"},
                {"type": "text", "text": "Avalie a imagem enviada a seguir."},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        )
    ]
    
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Erro ao processar a imagem: {str(e)}"


# Exemplo de uso:
#link = "https://drive.google.com/file/d/1-JKXBvocylsq_Czbq0AIdr0ncEDy3wGh/view?usp=sharing"
#image_url = link_drive_direto(link)
#descricao = analisar_imagem_carga(image_url)
#print("Descrição da imagem:", descricao)