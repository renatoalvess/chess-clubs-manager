from werkzeug.security import generate_password_hash
import mysql.connector
from db.db import conexao_db
from config import admin_password


conexao = conexao_db()


def criar_admin(user_id, username, senha):
    # Conectar ao banco de dados
    conexao = conexao_db()
    cursor = conexao.cursor()

    # Verificar se o administrador já existe
    consulta = "SELECT * FROM users WHERE username = %s AND is_admin = %s"
    cursor.execute(consulta, (username, True))
    admin_existente = cursor.fetchone()

    if admin_existente:
        print("Administrador já existe.")
        return

    # Criptografar a senha
    senha_criptografada = generate_password_hash(senha)

    # Criar o novo administrador
    consulta_inserir = """
    INSERT INTO users (id, username, password, is_admin)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(consulta_inserir,
                   (user_id, username, senha_criptografada, True))
    conexao.commit()

    print("Administrador criado com sucesso!")

    # Fechar conexão
    cursor.close()
    conexao.close()


# Exemplo de chamada
criar_admin(1, "admin", admin_password)
