import os
import requests
import json
from fpdf import FPDF
from datetime import datetime

def create_product():
    os.makedirs('products', exist_ok=True)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    # URL oficial v1 (mais estável)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Estrutura de dados exata que o Google pede
    payload = {
        "contents": [{
            "parts": [{
                "text": "Write a 500-word professional guide in English about digital marketing tips."
            }]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    print(f"🛰️ Testando conexão com a nova chave...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            # Pega o texto da resposta
            text = data['candidates'][0]['content']['parts'][0]['text']
            
            # Gera o PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            clean_text = text.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, clean_text)
            
            filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            pdf.output(filename)
            print(f"✅ SUCESSO ABSOLUTO! Arquivo criado: {filename}")
        else:
            print(f"❌ ERRO {response.status_code}: {response.text}")
            # Se der 404 de novo, vamos tentar a URL v1beta automaticamente
            print("🔄 Tentando caminho alternativo (v1beta)...")
            url_beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            response_beta = requests.post(url_beta, headers=headers, json=payload)
            if response_beta.status_code == 200:
                print("✅ Sucesso pelo caminho alternativo!")
            else:
                raise Exception(f"Falha total: {response_beta.status_code}")
                
    except Exception as e:
        print(f"❌ Falha na execução: {e}")
        raise

if __name__ == "__main__":
    create_product()
