from app import app
from app.configs import db
from app.models.usuario_sistema import UsuarioSistema
from app.templates import desempenho_geral, historico_producao, index, interface, lista, producao_energia, \
    status_tempo_real, alertas_notificacoes
from app.templates.usuario import login, cadastro
from app.templates.formularios import cadastro_banco_parte_1, cadastro_banco_parte_2
from flask import request


@app.route('/')
@app.route('/index')
def indice():
    return index.index.index()


@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        # Obter os dados do formulário enviado pela interface Dash
        nome = request.form['username-input']
        empresa = request.form['company-input']
        email = request.form['email-input']
        senha = request.form['password-input']

        # Criar um novo objeto UsuarioSistema com os dados recebidos
        novo_usuario = UsuarioSistema(nome_usuario=nome, nome_empresa=empresa, email_login=email, senha_login=senha)

        # Adicionar o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        # Retornar uma resposta para a interface Dash
        return 'Usuário cadastrado com sucesso!'



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
    return cadastro_banco_parte_1.cad_banco_1.index()
