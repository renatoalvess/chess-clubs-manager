from flask_login import LoginManager
from login.login import load_user

login_manager = LoginManager()


def init_app(app):
    """Inicializa o login manager com a aplicação"""
    login_manager.init_app(app)
    login_manager.login_view = "login.login"

    login_manager.login_message = ""


# Configura a função de carregamento do usuário
login_manager.user_loader(load_user)
