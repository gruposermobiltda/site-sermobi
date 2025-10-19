import csv
import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuração do e-mail (usando Gmail como exemplo)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gruposermobiltda@gmail.com'      # <-- Troque aqui
app.config['MAIL_PASSWORD'] = 'vwia bwng ysea ewou'         # <-- Troque aqui
app.config['MAIL_DEFAULT_SENDER'] = 'gruposermobiltda@gmail.com' # <-- Troque aqui

mail = Mail(app)

linhas = [
    "Linha 001 - Centro / Bairro A",
    "Linha 002 - Centro / Bairro B",
    "Linha 003 - Centro / Bairro C"
]

@app.route("/")
def home():
    return render_template("index.html", linhas=linhas)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/servicos")
def servicos():
    return render_template("servicos.html")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")

        # Enviar e-mail com HTML
        msg = Message(
            subject=f"Novo contato de {nome} via Grupo SerMobi",
            recipients=["gruposermobiltda@gmail.com"]
        )
        msg.body = f"Nome: {nome}\nEmail: {email}\nMensagem:\n{mensagem}"
        msg.html = f"""
        <h2>Nova mensagem de contato</h2>
        <p><strong>Nome:</strong> {nome}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Mensagem:</strong><br>{mensagem}</p>
        """
        mail.send(msg)

        # Salvar no CSV
        arquivo_csv = 'contatos.csv'
        existe = os.path.isfile(arquivo_csv)

        with open(arquivo_csv, 'a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            if not existe:
                writer.writerow(['Nome', 'Email', 'Mensagem'])
            writer.writerow([nome, email, mensagem])

        return render_template("contato.html", enviado=True, nome=nome)

    return render_template("contato.html", enviado=False)

if __name__ == "__main__":
    app.run(debug=True)