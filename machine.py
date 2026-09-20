import os
import google.generativeai as genai
from fpdf import FPDF
from datetime import datetime

# Configura a IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def create_product():
    print(f"🚀 Iniciando criação: {datetime.now()}")
    
    # IA gera o conteúdo em Inglês
    prompt = "Create a high-value digital guide in English about 'Passive Income with AI'. Include Title, Intro, 5 strategies and Conclusion."
    response = model.generate_content(prompt)
    
    # Cria o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Automated Digital Product", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    clean_text = response.text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    
    if not os.path.exists('products'):
        os.makedirs('products')
        
    filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    print(f"✅ Salvo em: {filename}")

if __name__ == "__main__":
    create_product()
