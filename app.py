from flask import Flask
from db.db import criar_tabela_clubes, criar_tabela_players, criar_database, criar_tabela_matches, criar_tabela_users
from clubs.clubs import clubs_blueprint
from players.players import players_blueprint
from rating.rating import rating_blueprint
from ranking.ranking import ranking_blueprint
from login.login import login_blueprint, load_user
from flask_login import LoginManager
from login.auth import init_app
from register.register import register_blueprint
from db.db import conexao_db


app = Flask(__name__)

# Configura o Flask-Login
app.secret_key = '951753852456'

# Inicializa o LoginManager
init_app(app)

app.register_blueprint(clubs_blueprint)
app.register_blueprint(players_blueprint)
app.register_blueprint(rating_blueprint)
app.register_blueprint(ranking_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)

if __name__ == '__main__':
    criar_database()
    criar_tabela_clubes()
    criar_tabela_players()
    criar_tabela_matches()
    criar_tabela_users()
    criar_tabela_users()
    app.run(debug=True)
