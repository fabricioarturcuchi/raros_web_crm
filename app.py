from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "segredo"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # pegar campos do formulário aqui
        # validar e salvar os dados

        return redirect("/")  # ou render_template com feedback
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
