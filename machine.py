import os
import requests
import json

def create_product():
    print("🚀 Ligando motor com a chave de projeto...")
    
    # 1. Recupera a chave API configurada nas variáveis de ambiente do GitHub Actions
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERRO: A variável de ambiente GEMINI_API_KEY não foi configurada no GitHub.")
        raise Exception("Chave de API ausente.")

    # 2. Define o modelo e usa a API v1beta (corrige o erro 404)
    model = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 3. Exemplo de payload estruturado (ajuste o prompt conforme a necessidade do seu motor)
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Gere uma lista de ideias de produtos digitais lucrativos para vender por 1 dólar."}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # Se falhar, exibe o erro detalhado para facilitar o diagnóstico
        if response.status_code != 200:
            print(f"❌ ERRO {response.status_code}: {response.text}")
            print("\nDICA: Se o erro persistir mesmo na v1beta, certifique-se de que a 'Generative Language API' está ATIVADA no Console do Google Cloud.")
            raise Exception("Falha na conexão com o Google.")
            
        # 4. Processa a resposta de sucesso
        data = response.json()
        resultado = data['candidates'][0]['content']['parts'][0]['text']
        print("✅ Motor rodou com sucesso! Resposta recebida:")
        print(resultado)
        return resultado

    except Exception as e:
        if "Falha na conexão" not in str(e):
            print(f"❌ Ocorreu uma exceção inesperada: {e}")
        raise

if __name__ == "__main__":
    create_product()
