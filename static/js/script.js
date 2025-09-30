document.getElementById("emailForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultadoDiv = document.getElementById("resultado");
        if (data.erro) {
            resultadoDiv.innerHTML = `<br><p style="color:red;">Erro: ${data.erro}</p>`;
        } else {
            resultadoDiv.innerHTML = `
                <br>
                <h3 class="apresentacao__conteudo__links__subtitulo">O email tem a categoria:</h3>
                <p>${data.categoria}</p>
                <br>
                <h3 class="apresentacao__conteudo__links__subtitulo">Resposta automática sugerida para esse email:</h3>
                <pre>${data.respostaSugerida}</pre>
                <br>
                <h3 class="apresentacao__conteudo__links__subtitulo">Mensagem:</h3>
                <p>${data.mensagem}</p>
                <br>
                <h3 class="apresentacao__conteudo__links__subtitulo">Tipo de arquivo:</h3>
                <p>${data.tipoDeArquivo}</p>
            `;
        }
    })
    .catch(error => {
        console.error("Erro:", error);
        document.getElementById("resultado").innerHTML = "<br><p style='color:red;'>Ocorreu um erro ao enviar o email.</p>";
    });

    document.getElementById("file").value = "";
    document.getElementById("textContent").value = "";
});