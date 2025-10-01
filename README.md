<h1>Classificador de Email</h1>

<h2> 📌 Descrição do projeto</h2>

Aplicação web simples que utiliza inteligência artificial para:
1. **Classificar** emails em categorias predefinidas (Produtivo ou Improdutivo).
2. **Sugerir automaticamente** uma resposta para o email baseado na classificação realizada.
  
Categorias de Classificação:
- **Produtivo:** Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
- **Improdutivo:** Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).

<h2> :hammer: Requisitos do projeto </h2>

**1. Interface Web (HTML)**

**Formulário de Upload:**

- Permitir o upload de arquivos de email em formatos .txt ou .pdf ou a inserção direta de texto de emails.
- Botão para enviar o documento/email para processamento.

**Exibição dos Resultados:**

- Mostrar a categoria atribuída ao email (Produtivo ou Improdutivo).
- Exibir a resposta automática sugerida pelo sistema.

**2. Backend em Python**

**Leitura e Processamento:**

- Desenvolver um script em Python que leia o conteúdo dos emails enviados.
- Utilizar técnicas de processamento de linguagem natural (NLP) para pré-processar o texto (remoção de stop words, stemming/lemmatização, etc.).

**Classificação e Resposta:**

- Implementar um algoritmo de classificação que categorize o conteúdo em **Produtivo** ou **Improdutivo**.
- Utilizar uma API de AI para:
  - Determinar a categoria do email.
  - Sugerir uma resposta automática adequada à categoria identificada.

**Integração com a Interface Web:**

- Conectar o backend com a interface HTML para receber entradas e exibir resultados.

**3. Hospedagem na Nuvem**

**Deploy da Aplicação:**

- Hospedar a aplicação web em uma plataforma de nuvem gratuita.

<h2> 🧠 Tecnologias utilizadas </h2>

- Python 3
- Flask
- Google Generative AI
- PyPDF2
- NLTK (Natural Language Toolkit)
- HTML
- CSS
- Flex-box
- JavaScript

<h2> 📁 Acesso ao projeto </h2>

**1. Para acessar o projeto localmente faça:**
- Instale o Python: Baixe e instale o interpretador do Python a partir do site oficial, python.org.
- Crie e ative o ambiente virtual: Use o interpretador do Python já instalado para criar um ambiente isolado para o projeto usando: <br>
  `python -m venv venv`
- Instale as dependências: Com o ambiente virtual ativado, use o comando abaixo para instalar as bibliotecas do projeto: <br>
  `pip install -r requirements.txt`

**2. Hospedagem na Nuvem:**
<br>

Após acessar o projeto clique no botão "Procurar..." na página principal da aplicação e utilize os arquivos .txt e .pdf localizados na pasta [`samples/`](https://github.com/camlopes/classificador-email/tree/master/samples) para enviar exemplos de emails que serão classificados e respondidos pela IA. 