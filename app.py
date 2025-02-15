from flask import Flask, render_template, request, send_file
import pdfkit
import os

app = Flask(__name__)

# Configuração do caminho do wkhtmltopdf
WKHTMLTOPDF_PATH = '/usr/bin/wkhtmltopdf'  # Altere este caminho conforme necessário
pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/gerar_procuracao', methods=['POST'])
def gerar_procuracao():
    dados = request.form.to_dict()
    html = render_template('procuracao.html', **dados)
    
    # Salvar o HTML temporariamente
    temp_html_path = os.path.join("templates", "temp.html")
    with open(temp_html_path, "w", encoding="utf-8") as file:
        file.write(html)
    
    # Converter HTML para PDF
    pdf_path = "procuracao.pdf"
    pdfkit.from_file(temp_html_path, pdf_path, configuration=pdfkit_config)
    os.remove(temp_html_path)  # Remover arquivo temporário
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
