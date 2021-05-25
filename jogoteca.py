from logging import debug, log
from flask import Flask, request, render_template, redirect, session
from flask.helpers import flash, url_for

app = Flask(__name__)
app.secret_key = 'alura'

class Jogo:
    def __init__(self, nome, categoria, console) -> None:
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha) -> None:
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('levi', 'Levi Pedreira', '1234')
usuario2 = Usuario('nico', 'Nico', '7a1')
usuario3 = Usuario('flavio', 'Flavio', 'javascript')

usuarios = {
    usuario1.id: usuario1,
    usuario2.id: usuario2,
    usuario3.id: usuario3
}

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GameBoy')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
lista = [jogo1, jogo2, jogo3]

@app.route('/index')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if(session['usuario_logado'] == None):
        flash('Faça o login primeiro!')
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    if(session['usuario_logado'] == None):
        proxima = request.args.get('proxima')
        return render_template('login.html', proxima=proxima)
    else:
        flash('O usuário ' + usuarios[session['usuario_logado']].nome + ' está logado na sessão!')
        return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST'])
def autenticar():         
    if(request.form['usuario'] in usuarios):
        usuario = usuarios[request.form['usuario']]       
        if(usuario.senha == request.form['senha']):
            session['usuario_logado'] = usuario.id
            flash('Olá ' + usuario.nome + ', você logou com sucesso!')
            proxima = request.form['proxima']
            return redirect(proxima)
        else:
            flash('Login e/ou senha incorreto(s)!')
            return redirect(url_for('login'))
    else:
        flash('Login e/ou senha incorreto(s)!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Você saiu da sessão!')
    return redirect (url_for('index')) 

app.run(debug=True)