import os
import requests
import json
from fpdf import FPDF
from datetime import datetime

def create_product():
    os.makedirs('products', exist_ok=True)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    # Tentando a versão estável v1 que costuma aceitar chaves de projeto (AQ)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Write a 500-word guide about digital marketing in English."}]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    print(f"🚀 Testando conexão com chave {api_key[:5]}...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, clean_text)
        
        filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        pdf.output(filename)
        print(f"✅ SUCESSO! PDF criado: {filename}")
    else:
        print(f"❌ ERRO {response.status_code}: {response.text}")
        # Se der erro 404 aqui, a chave AQ não é compatível com esse método.
        raise Exception("A chave AQ falhou. Precisamos da chave AIza.")

if __name__ == "__main__":
    create_product()
