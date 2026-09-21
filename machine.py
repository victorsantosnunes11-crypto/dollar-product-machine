import os
import requests
import json
import sys
from fpdf import FPDF
from datetime import datetime

def create_product():
    # 1. Garante a pasta e o arquivo de controle
    os.makedirs('products', exist_ok=True)
    with open('products/.gitkeep', 'w') as f:
        f.write('')
    
    print(f"🚀 Iniciando criação (Versão Estável v1): {datetime.now()}")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Erro: Chave GEMINI_API_KEY não configurada!")
        sys.exit(1)

    # Mudamos de v1beta para v1 (mais estável)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = "Write a professional 500-word guide in English about productivity. Include a title and 5 tips."
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # Se a v1 falhar, tentamos uma alternativa automática
        if response.status_code == 404:
            print("🔄 Tentando URL alternativa...")
            url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            response = requests.post(url_alt, headers=headers, json=payload, timeout=30)

        response.raise_for_status()
        data = response.json()
        product_text = data['candidates'][0]['content']['parts'][0]['text']
        
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        if 'response' in locals():
            print(f"Resposta do Servidor: {response.text}")
        sys.exit(1)

    # 2. Gerar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Digital Guide - Automated Edition", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    clean_text = product_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    
    filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    
    if os.path.exists(filename):
        print(f"✅ SUCESSO ABSOLUTO: {filename} criado!")
    else:
        print("❌ Erro ao gravar PDF.")
        sys.exit(1)

if __name__ == "__main__":
    create_product()
