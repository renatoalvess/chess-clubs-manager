import mysql.connector
from config import db_password



def conexao_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=db_password,
        database='bdchess'
    )


def criar_database():
    """Conecta e cria a base de dados."""
    conexao = conexao_db()
    cursor = conexao.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS bdchess")
    conexao.commit()

    cursor.close()
    conexao.close()


def criar_tabela_clubes():
    """Conecta ao banco de dados e cria a tabela 'clubs' no banco de dados se não existir."""
    conexao = conexao_db()

    cursor = conexao.cursor()  # Cursor: executa os comandos da conexão.

    cursor.execute('''CREATE TABLE IF NOT EXISTS clubs (
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   name VARCHAR(255) NOT NULL UNIQUE,
                   creation_date DATE NOT NULL,
                   status ENUM('Ativo', 'Excluído') DEFAULT 'Ativo')''')
    conexao.commit()

    cursor.close()
    conexao.close()


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
