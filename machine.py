import os
import requests
import json
import sys
from fpdf import FPDF
from datetime import datetime

def create_product():
    os.makedirs('products', exist_ok=True)
    with open('products/.gitkeep', 'w') as f:
        f.write('')
    
    print(f"🚀 Iniciando Caçador de Modelos: {datetime.now()}")
    
    # Limpa a chave de possíveis espaços em branco
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("❌ Erro: Chave GEMINI_API_KEY não configurada!")
        sys.exit(1)

    # Lista de modelos para testar (do mais novo ao mais estável)
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-pro"
    ]
    
    product_text = None
    
    for model in models_to_try:
        print(f"🔎 Tentando modelo: {model}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": "Write a 500-word professional guide in English about productivity tips."}]}]
        }
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                product_text = data['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Sucesso com o modelo: {model}!")
                break
            else:
                print(f"⚠️ {model} falhou (Erro {response.status_code})")
        except Exception as e:
            print(f"⚠️ Erro ao testar {model}: {e}")

    if not product_text:
        print("❌ Nenhum modelo funcionou. Verifique se sua conta do Google AI Studio está ativa.")
        sys.exit(1)

    # 2. Gerar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Digital Guide - Automated Edition", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    # Limpeza de texto para PDF
    clean_text = product_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    
    filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    
    if os.path.exists(filename):
        print(f"🏆 VITÓRIA! Arquivo criado: {filename}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    create_product()
