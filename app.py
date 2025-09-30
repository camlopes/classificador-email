from flask import Flask, request, render_template, jsonify
import PyPDF2
import google.generativeai as genai
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")
genai.configure(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

def pre_processamento_email(email_conteudo):
    email_conteudo_minusculas = email_conteudo.lower()
    
    email_tokens = word_tokenize(email_conteudo_minusculas, language='portuguese')
    
    stop_words = set(stopwords.words("portuguese"))
    email_tokens_sem_stopwords = [t for t in email_tokens if t.isalpha() and t not in stop_words]
    
    stemmer = RSLPStemmer()
    pre_processado_email = [stemmer.stem(t) for t in email_tokens_sem_stopwords]

    return " ".join(pre_processado_email)

def prompt_ia(email_pre_processado, email_original):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt_categoria = """
        De acordo com as categorias de emails abaixo: 
        Produtivo: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
        Improdutivo: Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).
        Qual é a categoria do email a seguir? 
        
        Atenção: Responda somente com a palavra "Produtivo" ou "Improdutivo".
        
        """ + email_pre_processado

    prompt_resposta = """
        Responda o "Email pre processado" abaixo exatamente com o inicio e final mostrados:
        
        Inicio padrao da resposta do email:
        Assunto: Re: [assunto que esta informado em "Email original" abaixo]
        Para: [email da pessoa que enviou o email. Essa informacao esta em "Email original"]
        
        Final padrao da resposta do email:
        Atenciosamente,
        resposta_ti@empresatm.com.br
        Suporte
        empresaTM

        Email original:
        """ + email_original + """
        
        Email pre processado:
        """ + email_pre_processado

    try:
        categoria = model.generate_content(prompt_categoria).text.strip()

        if categoria == "Improdutivo":
            prompt_resposta += """ 
            Responda com uma mensagem automatica de acordo com o assunto do email que esta em "Email original" """
        
        resposta_sugerida = model.generate_content(prompt_resposta).text.strip()  
        return categoria, resposta_sugerida
    except Exception as e:
        print(f"Erro ao chamar a Gemini API: {e}")
        return None, None

@app.route("/upload", methods=["POST"])
def upload_file():
    conteudo_texto = request.form.get("textContent", "").strip()
    file = request.files.get("file")

    email_conteudo = ""

    if conteudo_texto:
        email_conteudo = conteudo_texto
        tipo_de_arquivo = "caixa de texto"
    elif file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        if filename.endswith(".txt"):
            tipo_de_arquivo = ".txt"
            with open(filepath, "r", encoding="utf-8") as f:
                email_conteudo = f.read()

        elif filename.endswith(".pdf"):
            tipo_de_arquivo = ".pdf"
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    email_conteudo += page.extract_text() or ""

    if email_conteudo == "":
        return jsonify({"erro": "Nenhum conteúdo foi enviado."}), 400
    
    email_pre_processado = pre_processamento_email(email_conteudo)

    categoria, resposta_sugerida = prompt_ia(email_pre_processado, email_conteudo)
    if categoria == None and resposta_sugerida == None:
        return jsonify({"erro": "Erro ao chamar a Gemini API"}), 400

    return jsonify({
        "categoria": categoria,
        "respostaSugerida": resposta_sugerida,
        "tipoDeArquivo": tipo_de_arquivo,
        "mensagem": "Arquivo/texto processado com sucesso!"
    })

if __name__ == "__main__":
    app.run(debug=True)
