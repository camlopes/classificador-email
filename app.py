from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    text_content = request.form.get("textContent", "").strip()
    file = request.files.get("file")

    email_content = ""
    tipo_de_arquivo = ""

    if text_content:
        email_content = text_content
        tipo_de_arquivo = "caixa de texto"
    elif file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        if filename.endswith(".txt"):
            tipo_de_arquivo = ".txt"
            with open(filepath, "r", encoding="utf-8") as f:
                email_content = f.read()

        elif filename.endswith(".pdf"):
            tipo_de_arquivo = ".pdf"
            import PyPDF2
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    email_content += page.extract_text() or ""

    if not email_content:
        return jsonify({"erro": "Nenhum conteúdo foi enviado."}), 400
    
    return jsonify({
        "conteudo": email_content,
        "tipoDeArquivo": tipo_de_arquivo,
        "mensagem": "Arquivo/texto processado com sucesso!"
    })

if __name__ == "__main__":
    app.run(debug=True)
