import os
import requests
import json
from fpdf import FPDF
from datetime import datetime

def create_product():
    print(f"🚀 Iniciando criação: {datetime.now()}")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Erro: GEMINI_API_KEY não encontrada nos Segredos!")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Prompt mais seguro para evitar bloqueios de filtro
    prompt = "Write a helpful 500-word guide about personal productivity and time management in English. Include a title and 5 tips."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "safetySettings": [ # Desativa filtros sensíveis que bloqueiam por engano
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code != 200:
        print(f"❌ Erro na API: {response.status_code} - {response.text}")
        return

    data = response.json()
    try:
        product_text = data['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        print(f"❌ Resposta da API inesperada ou vazia: {data}")
        return

    # Cria a pasta antes de gerar o PDF
    os.makedirs('products', exist_ok=True)
    
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
        print(f"✅ SUCESSO: Arquivo {filename} criado com {len(clean_text)} caracteres.")
    else:
        print("❌ Erro: O arquivo PDF não foi gravado no disco.")

if __name__ == "__main__":
    create_product()
