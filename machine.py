import os
import requests
import json
from fpdf import FPDF
from datetime import datetime

def create_product():
    os.makedirs('products', exist_ok=True)
    # Pega a chave (seja ela AIza ou AQ)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    # URL estável v1 - Funciona com chaves de projeto (AQ)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Write a short professional guide about digital success in English."}]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    print(f"🚀 Ligando motor com a chave de projeto...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # Limpa o texto para evitar erro de PDF
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, clean_text)
        
        filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        pdf.output(filename)
        print(f"✅ SUCESSO! Produto criado: {filename}")
    else:
        print(f"❌ ERRO {response.status_code}: {response.text}")
        if response.status_code == 404:
            print("DICA: Vá no Google Cloud e clique em ATIVAR na 'Generative Language API'.")
        raise Exception("Falha na conexão com o Google.")

if __name__ == "__main__":
    create_product()
