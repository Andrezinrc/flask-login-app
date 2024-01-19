from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from form import FormLogin, FormCadastro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    csenha = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def login():
    form = FormLogin()

    if form.validate_on_submit():
             pass

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = User.query.filter_by(email=email, senha=senha).first()

        if usuario:
            login_user(usuario)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('login_sucesso'))
        else:
            flash('Usuario ou senha invalidos', 'danger')

    return render_template("login.html", form=form)

@app.route("/login_sucesso", methods=['GET'])
@login_required
def login_sucesso():
    return f"Login feito com sucesso para o usuario {current_user.nome}"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():

    form = FormCadastro()

    if form.validate_on_submit():
             pass

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        csenha = request.form['csenha']

        if senha == csenha:
            novo_usuario = User(nome=nome, email=email, senha=senha, csenha=csenha)
            db.session.add(novo_usuario)
            db.session.commit()

            flash('Cadastro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))

    return render_template("cadastro.html", form=form)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
