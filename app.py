from flask import Flask, render_template, request, redirect, flash
import os
import openpyxl

app = Flask(__name__)
app.secret_key = "segredo"

# Função para salvar no Excel
def salvar_lead_excel(dados):
    arquivo = "leads.xlsx"
    if not os.path.exists(arquivo):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Leads"
        ws.append([
            "Nome/Razão Social", "Tipo Documento", "Documento", "Telefone", "E-mail",
            "CEP", "Rua", "Número", "Bairro", "Cidade", "Bem", "Valor", "Parcela",
            "Status", "Origem"
        ])
        wb.save(arquivo)

    wb = openpyxl.load_workbook(arquivo)
    ws = wb["Leads"]
    ws.append(dados)
    wb.save(arquivo)

# Página principal com formulário
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

            # Validações
            if not nome_razao or not tipo_doc or not documento or not telefone or not cep or not bem or valor <= 0:
                flash("Preencha todos os campos obrigatórios corretamente.", "danger")
                return redirect("/")

            # Cálculo da parcela
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

            # Salvar no Excel
            salvar_lead_excel([
                nome_razao, tipo_doc, documento, telefone, email, cep, rua,
                numero, bairro, cidade, bem, valor, parcela, status, origem
            ])

            flash(f"Lead cadastrado com sucesso! Parcela: R$ {parcela:.2f}", "success")
            return redirect("/")
        except Exception as e:
            flash(f"Erro ao processar os dados: {e}", "danger")
            return redirect("/")
    return render_template("index.html")

# Rota para exibir leads
@app.route("/leads")
def visualizar_leads():
    leads = []
    arquivo = "leads.xlsx"
    if os.path.exists(arquivo):
        wb = openpyxl.load_workbook(arquivo)
        ws = wb["Leads"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            leads.append(row)
    return render_template("leads.html", leads=leads)

# Rodar app local ou na Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
