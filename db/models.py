import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db.db import conexao_db


conexao = conexao_db()


class User(UserMixin):
    def __init__(self, user_id, username, password, is_admin=False):
        self.id = user_id
        self.username = username
        self.password = password
        self.is_admin = is_admin  # Atributo adicionado para definir se é admin ou não

    def get_id(self):
        return str(self.id)
