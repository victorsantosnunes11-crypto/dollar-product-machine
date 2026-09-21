
import os
import requests
import json
import sys
from fpdf import FPDF
from datetime import datetime

def create_product():
    # 1. Forçar a criação da pasta antes de qualquer coisa
    os.makedirs('products', exist_ok=True)
    with open('products/.gitkeep', 'w') as f: # Garante que o Git veja a pasta
        f.write('')
    
    print(f"🚀 Iniciando criação: {datetime.now()}")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Erro: Chave GEMINI_API_KEY não configurada nos Secrets!")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = "Write a 500-word professional guide in English about productivity. Include a title and 5 tips."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status() # Força erro se o status não for 200
        data = response.json()
        product_text = data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"❌ Erro Crítico na API: {e}")
        if 'response' in locals():
            print(f"Detalhes: {response.text}")
        sys.exit(1) # Faz o GitHub parar aqui e mostrar erro vermelho

    # 2. Gerar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Digital Content - Automated Edition", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    clean_text = product_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    
    filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    
    if os.path.exists(filename):
        print(f"✅ SUCESSO: {filename} criado!")
    else:
        print("❌ Erro: PDF não foi gerado.")
        sys.exit(1)

if __name__ == "__main__":
    create_product()
