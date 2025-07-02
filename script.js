function mascaraDocumento() {
    let tipo = document.getElementById('tipo_doc').value;
    let doc = document.getElementById('documento');
    doc.maxLength = tipo === "CPF" ? 14 : 18;
    doc.value = '';
}

function buscarEndereco() {
    let cep = document.getElementById('cep').value.replace("-", "");
    if (cep.length !== 8) return;
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('rua').value = data.logradouro || '';
            document.getElementById('bairro').value = data.bairro || '';
            document.getElementById('cidade').value = data.localidade || '';
        });
}

function calcularParcela() {
    let valor = parseFloat(document.getElementById('valor').value);
    let tipo = document.getElementById('bem').value;
    let parcela = 0;
    if (tipo === "Automóvel" && valor >= 65000) {
        parcela = (valor * 1.16) / 84;
    } else if (tipo === "Imóvel" && valor >= 200000) {
        parcela = (valor * 1.22) / 220;
    } else {
        document.getElementById('parcela').value = "Valor abaixo do mínimo";
        return;
    }
    document.getElementById('parcela').value = parcela.toFixed(2).replace(".", ",");
}
