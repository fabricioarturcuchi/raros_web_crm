from flask import Flask, render_template, request, redirect, flash
import os

app = Flask(__name__)
app.secret_key = "segredo"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            nome_razao = request.form.get("nome_razao")
            tipo_doc = request.form.get("tipo_doc")
            documento = request.form.get("documento")
            telefone = request.form.get("telefone")
            email = request.form.get("email")
            cep = request.form.get("cep")
            rua = request.form.get("rua")
            numero = request.form.get("numero")
            bairro = request.form.get("bairro")
            cidade = request.form.get("cidade")
            bem = request.form.get("bem")
            valor_raw = request.form.get("valor", "0").replace(",", ".")
            valor = float(valor_raw) if valor_raw else 0
            status = request.form.get("status")
            origem = request.form.get("origem")

            # Validações simples
            if not nome_razao or not tipo_doc or not documento or not telefone or not cep or not bem or valor <= 0:
                flash("Preencha todos os campos obrigatórios corretamente.", "danger")
                return redirect("/")

            # Regras parcela
            if bem == "Automóvel":
                if valor < 65000:
                    flash("Valor mínimo para Automóvel é R$ 65.000,00", "danger")
                    return redirect("/")
                parcela = round((valor * 1.16) / 84, 2)
            elif bem == "Imóvel":
                if valor < 200000:
                    flash("Valor mínimo para Imóvel é R$ 200.000,00", "danger")
                    return redirect("/")
                parcela = round((valor * 1.22) / 220, 2)
            else:
                parcela = 0

            # Aqui você pode salvar os dados em Excel ou banco local (ainda não implementado)

            flash(f"Lead cadastrado com sucesso! Parcela: R$ {parcela:.2f}", "success")
            return redirect("/")
        except Exception as e:
            flash(f"Erro ao processar os dados: {e}", "danger")
            return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
