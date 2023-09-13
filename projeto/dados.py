#coding:utf-8

from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)
app.app_context().push()

class Doador(db.Model):

    __tablename__ = 'doadores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    cpf = db.Column(db.String)
    endereco = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    numCarteira= db.Column(db.String)

    def __init__(self, nome, cpf, endereco, email, telefone, numCarteira):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.email = email
        self.telefone = telefone
        self.numCarteira = numCarteira

db.create_all()

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        endereco = request.form.get("endereco")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        numCarteira = request.form.get("numCarteira")

        if nome and cpf and endereco and email and telefone and numCarteira:
            d = Doador(nome, cpf, endereco, email, telefone, numCarteira)
            db.session.add(d)
            db.session.commit()


        return redirect(url_for("index"))
    
@app.route("/lista")
def lista():
    doadores = Doador.query.all()
    return render_template("lista.html", doadores=doadores)

@app.route("/excluir/<int:id>")
def excluir(id):
    doador = Doador.query.filter_by(id=id).first()

    db.session.delete(doador)
    db.session.commit()

    doadores = Doador.query.all()
    return render_template("lista.html", doadores=doadores)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    doador = Doador.query.filter_by(id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        numCarteira = request.form.get("numCarteira")

        if nome and endereco and email and telefone and numCarteira:
            doador.nome = nome
            doador.endereco = endereco
            doador.email = email
            doador.telefone = telefone
            doador.numCarteira = numCarteira

            db.session.commit()

            return redirect(url_for("lista"))
        
    return render_template("atualizar.html", doador=doador)    

if __name__ == '__main__':
    app.run(debug=True)