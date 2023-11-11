from app import app
from app.templates import desempenho_geral, historico_producao, index, interface, lista, producao_energia, \
    status_tempo_real, alertas_notificacoes
from app.templates.usuario import login


@app.route('/')
@app.route('/index')
def indice():
    return index.index.index()


@app.route('/interface')
def interfaces():
    return interface.interface.index()


@app.route('/lista')
def listas():
    return lista.lista.index()


@app.route('/login')
def log():
    return login.login_page.index()


@app.route('/desempenho_geral')
def desG():
    return desempenho_geral.desempenho_geral.index()


@app.route('/producao_energia')
def prod_energia():
    return producao_energia.producao_energia.index()


@app.route("/status_tempo_real")
def stts_tmp_rl():
    return status_tempo_real.status_tempo_real.index()


@app.route("/historico_producao")
def hist_prod():
    return historico_producao.historico_producao.index()


@app.route("/alertas_notificacoes")
def alts_ntf():
    return alertas_notificacoes.alertas_notificacoes.index()


@app.route("/formulario_db")
def formulario_db():
    return db_form.cad_banco_1.index()
