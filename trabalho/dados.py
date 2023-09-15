#Coding: UTF-8

#Importando os arquivos do Flask e outros comandos;

from flask import Flask, render_template, request, url_for, redirect

#Conectando com o banco de dados;

from flask_sqlalchemy import SQLAlchemy

#Criando a aplicação Flask e conectando com o banco de dados.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)
app.app_context().push()

#Criando a classe 'Doador';

class Doador(db.Model):

    #Criando a tabela doadores no BD;

    __tablename__ = 'doadores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    cpf = db.Column(db.String)
    endereco = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    numCarteira= db.Column(db.String)

    # * 'id' não precisa do comando autoincrement no Flask;

    #Definindo os dados que serão registrados pelo usuário;

    def __init__(self, nome, cpf, endereco, email, telefone, numCarteira):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.email = email
        self.telefone = telefone
        self.numCarteira = numCarteira

#Comando para criar o banco de dados no 'db.sqlite';

db.create_all()

#Comandos para as rotas;
##Indo para o arquivo 'index.html';

@app.route("/index")
def index():
    return render_template("index.html")

#Indo para o arquivo 'login.html';

@app.route("/login")
def login():
    return render_template("login.html")

#Indo para o arquivo 'cadastro.html';

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

#Usando os comandos GET, POST para adicionar dados no BD;

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        endereco = request.form.get("endereco")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        numCarteira = request.form.get("numCarteira")

        #Comandos para adicionar os dados no BD;

        if nome and cpf and endereco and email and telefone and numCarteira:
            d = Doador(nome, cpf, endereco, email, telefone, numCarteira)
            db.session.add(d)
            db.session.commit()

        return redirect(url_for("cdSucesso"))
    
#Indo para o arquivo 'cdSucesso.html';
    
@app.route("/cdSucesso")
def cdSucesso():
    return render_template("cdSucesso.html")

##Indo para o arquivo 'lista.html';

@app.route("/lista")
def lista():
    doadores = Doador.query.all()
    return render_template("lista.html", doadores=doadores)

#Usando os comandos GET, POST para excluir dados no BD;

@app.route("/excluir/<int:id>")
def excluir(id):
    doador = Doador.query.filter_by(id=id).first()

    db.session.delete(doador)
    db.session.commit()

    doadores = Doador.query.all()
    return render_template("lista.html", doadores=doadores)

#Usando os comandos GET, POST para atualizar dados no BD;

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    doador = Doador.query.filter_by(id=id).first()

    #Comandos para atualizar os dados no BD;

    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        email = request.form.get("email")
        telefone = request.form.get("telefone")

        if nome and endereco and email and telefone:
            doador.nome = nome
            doador.endereco = endereco
            doador.email = email
            doador.telefone = telefone

            db.session.commit()

            return redirect(url_for("lista"))
        
    return render_template("atualizar.html", doador=doador)    

#Rodando o arquivo no servidor local;

if __name__ == '__main__':
    app.run(debug=True)

# * <- Observações