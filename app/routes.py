from app import app
from app.templates.desempenho_geral import desempenho_geral
from app.templates.index import index
from app.templates.interface import interface
from app.templates.lista import lista
from app.templates.login import login_page
from app.templates.producao_energia import producao_energia


@app.route('/')
@app.route('/index')
def indice():
    return index.index()


@app.route('/interface')
def interfaces():
    return interface.index()


@app.route('/lista')
def listas():
    return lista.index()


@app.route('/login')
def log():
    return login_page.index()


@app.route('/desempenho_geral')
def desG():
    return desempenho_geral.index()


@app.route('/producao_energia')
def prod_energia():
    return producao_energia.index()
