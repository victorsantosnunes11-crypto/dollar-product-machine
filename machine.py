import os
import requests
import json
from fpdf import FPDF
from datetime import datetime

def create_product():
    os.makedirs('products', exist_ok=True)
    
    # Pega a chave do segredo do GitHub
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    # URL da API (usando a versão estável)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Write a 500-word professional guide in English about productivity tips."}]
        }]
    }
    
    print("🚀 Chamando API...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        # Extrai o texto
        text = data['candidates'][0]['content']['parts'][0]['text']
        
        # Cria o PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, clean_text)
        
        filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        pdf.output(filename)
        print(f"✅ SUCESSO! Arquivo criado: {filename}")
    else:
        print(f"❌ ERRO {response.status_code}: {response.text}")
        raise Exception("Falha na API")

if __name__ == "__main__":
    create_product()
