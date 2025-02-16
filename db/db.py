import mysql.connector
from config import db_password
import os


def conexao_db():
    try:
        bdchess = mysql.connector.connect(
            host="mysql",
            user="root",
            password=os.environ.get("MYSQL_ROOT_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
        print("Conexão com o banco de dados estabelecida.")  # Mensagem de sucesso
        return bdchess
    except mysql.connector.Error as err:
        print(f"Erro na conexão: {err}")  # Imprime o erro *completo*
        return None



def criar_database():
    """Conecta e cria a base de dados."""
    conexao = conexao_db()

    if conexao:  # <--- Verifica se a conexão NÃO é None
        cursor = conexao.cursor()
        try: # tratamento de erro na criação do banco de dados
            cursor.execute("CREATE DATABASE IF NOT EXISTS bdchess")
            conexao.commit()
            print("Banco de dados criado ou existente.")
        except mysql.connector.Error as err:
            print(f"Erro na criação do banco de dados: {err}")
            conexao.rollback() # desfaz as alterações em caso de erro

        cursor.close()
        conexao.close()
    else:
        print("Falha ao conectar ao banco de dados. Impossível criar o banco.")


def criar_tabela_clubes():
    """Conecta ao banco de dados e cria a tabela 'clubs' no banco de dados se não existir."""
    conexao = conexao_db()

    if conexao:
        cursor = conexao.cursor()  # Cursor: executa os comandos da conexão.

        cursor.execute('''CREATE TABLE IF NOT EXISTS clubs (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    creation_date DATE NOT NULL,
                    status ENUM('Ativo', 'Excluído') DEFAULT 'Ativo')''')
        conexao.commit()

        cursor.close()
        conexao.close()
    else:
        print("Falha ao conectar ao banco de dados. Impossível criar o banco.")


def criar_tabela_players():
    """Conecta ao banco de dados e cria a tabela 'players' no banco de dados se não existir."""
    conexao = conexao_db()

    cursor = conexao.cursor()  # Cursor: executa os comandos da conexão.

    cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    birthdate DATE NOT NULL,
                    gender VARCHAR(20),
                    contact VARCHAR(30),
                    rating INT,
                    club_id INT,
                    status ENUM('Ativo', 'Excluído') DEFAULT 'Ativo',
                    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE SET NULL)''')
    conexao.commit()

    cursor.close()
    conexao.close()


def criar_tabela_matches():
    """Conecta ao banco de dados e cria a tabela 'matches' no banco de dados se não existir."""
    conexao = conexao_db()

    cursor = conexao.cursor()  # Cursor: executa os comandos da conexão.

    cursor.execute('''CREATE TABLE IF NOT EXISTS matches (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    player1_id INT NOT NULL,
                    player2_id INT NOT NULL,
                    result FLOAT NOT NULL,
                    date DATE NOT NULL,
                    FOREIGN KEY (player1_id) REFERENCES players(id),
                    FOREIGN KEY (player2_id) REFERENCES players(id))''')
    conexao.commit()

    cursor.close()
    conexao.close()


def criar_tabela_users():
    """Conecta ao banco de dados e cria a tabela 'users' no banco de dados se não existir."""
    conexao = conexao_db()

    cursor = conexao.cursor()  # Cursor: executa os comandos da conexão.

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE)''')
    conexao.commit()

    cursor.close()
    conexao.close()


def criar_tabela_notices():
    """Conecta ao banco de dados e cria a tabela 'notícias' no banco de dados se não existir."""
    conexao = conexao_db()

    cursor = conexao.cursor()  # Cursor: executa os comandos da conexão.

    cursor.execute('''CREATE TABLE IF NOT EXISTS notices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    imagem_url VARCHAR(300),
                    titulo VARCHAR(200) NOT NULL,
                    conteudo_html TEXT NOT NULL,
                    data_publicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conexao.commit()
    cursor.close()
    conexao.close()