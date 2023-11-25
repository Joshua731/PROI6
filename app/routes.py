from flask import request

from app import app
from app.configs import db
from app.models.usuario_sistema import UsuarioSistema
from app.templates import index, interface
from app.templates.usuario import cadastro


@app.route("/")
def redirecionar_home():
    return interface.interface.index()


@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        # Obter os dados do formulário enviado pela interface Dash
        nome = request.form['username-input']
        empresa = request.form['company-input']
        email = request.form['email-input']
        senha = request.form['password-input']

        # Criar um novo objeto UsuarioSistema com os dados recebidos
        novo_usuario = UsuarioSistema(
            nome_usuario=nome,
            nome_empresa=empresa,
            email_login=email,
            senha_login=senha
        )
        # Adicionar o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        # Retornar uma resposta para a interface Dash
        return index.index.index()
    return cadastro.cadastro.index()
