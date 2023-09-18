import sqlite3


def criar_tabela_usuarios():
    # Conecte-se ao banco de dados (ou crie o banco se não existir)
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Crie a tabela 'usuarios' se ela ainda não existir
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome_usuario TEXT NOT NULL,
                       senha TEXT NOT NULL)''')

    # Salve as alterações e feche a conexão com o banco de dados
    conn.commit()
    conn.close()


# Chame a função para criar a tabela
criar_tabela_usuarios()
