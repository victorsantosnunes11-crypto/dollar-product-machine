import os
from google import genai
from fpdf import FPDF
from datetime import datetime

# Configura o cliente oficial novo
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def create_product():
    print(f"🚀 Iniciando criação com motor novo: {datetime.now()}")
    
    # IA gera o conteúdo em Inglês usando o modelo estável
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Create a high-value digital guide in English about 'Passive Income with AI'. Include Title, Intro, 5 strategies and Conclusion."
    )
    
    # Cria o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Automated Digital Product", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    # Pega o texto da resposta nova
    clean_text = response.text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    
    if not os.path.exists('products'):
        os.makedirs('products')
        
    filename = f"products/product_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    print(f"✅ Produto gerado com sucesso: {filename}")

if __name__ == "__main__":
    create_product()
