import os
import requests
import json
from fpdf import FPDF
from datetime import datetime

def create_product():
    print(f"🚀 Iniciando criação direta via API: {datetime.now()}")
    
    api_key = os.environ["GEMINI_API_KEY"]
    # Usando a URL direta para evitar erros de biblioteca
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = "Create a high-value digital guide in English about 'Passive Income with AI'. Include Title, Intro, 5 strategies and Conclusion."
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    # Faz a requisição direta
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()
    
    if response.status_code != 200:
        print(f"❌ Erro na API: {data}")
        return

    # Extrai o texto da resposta
    product_text = data['candidates'][0]['content']['parts'][0]['text']
    
    # Cria o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Automated Digital Product", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    # Limpa o texto para o PDF
    clean_text = product_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    
    if not os.path.exists('products'):
        os.makedirs('products')
        
    filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    print(f"✅ Produto gerado com sucesso: {filename}")

if __name__ == "__main__":
    create_product()
