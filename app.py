from flask import Flask, render_template, request, redirect, flash
import openpyxl, os

app = Flask(__name__)
app.secret_key = 'r@ros_secret'
ARQUIVO_EXCEL = 'leads.xlsx'

def salvar_excel(dados):
    if not os.path.exists(ARQUIVO_EXCEL):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Leads"
        ws.append(["Nome","Tipo Doc","CPF/CNPJ","Telefone","Email","CEP","Rua","Número","Bairro","Cidade","Bem","Valor","Parcela","Status","Origem"])
        wb.save(ARQUIVO_EXCEL)
    wb = openpyxl.load_workbook(ARQUIVO_EXCEL)
    ws = wb["Leads"]
    ws.append(dados)
    wb.save(ARQUIVO_EXCEL)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = request.form
        salvar_excel([
            form["nome"], form["tipo_doc"], form["documento"], form["telefone"],
            form["email"], form["cep"], form["rua"], form["numero"],
            form["bairro"], form["cidade"], form["bem"], form["valor"],
            form["parcela"], form["status"], form["origem"]
        ])
        flash("Lead salvo com sucesso!", "success")
        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
