import mysql.connector
from werkzeug.security import generate_password_hash
from db.db import conexao_db

def criar_admin(username, senha):
    conexao = conexao_db()
    cursor = conexao.cursor()

    # Verifica se já existe um administrador
    cursor.execute("SELECT * FROM users WHERE is_admin = TRUE")
    admin_existente = cursor.fetchone()

    if admin_existente:
        print("Administrador já existe.")
        return

    # Criptografa a senha
    senha_criptografada = generate_password_hash(senha)

    # Insere o primeiro admin
    cursor.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)",
        (username, senha_criptografada, True)
    )
    
    conexao.commit()
    cursor.close()
    conexao.close()

    print("Administrador criado com sucesso!")
