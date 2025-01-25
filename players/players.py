from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
import mysql.connector
from db.db import conexao_db


conexao = conexao_db()


players_blueprint = Blueprint('players', __name__, template_folder='templates')


@players_blueprint.route("/")  # rota raiz
def index():
    return render_template("index.html")


# rota add_club/aceita POST e GET. (POST: envia dados p/ servidor e GET: solicitado dados do servidor)
@players_blueprint.route("/add_player", methods=["POST", "GET"])
def add_player():
    """Cadastra um novo jogador"""
    if request.method == "POST":
        # obtém o valor do campo de formulário com o nome "nome".
        name = request.form["nome"]
        # obtém o valor do campo de formulário com o nome "data_criacao".
        birthdate = request.form["data_nascimento"]
        gender = request.form["sexo"]
        contact = request.form["contato"]
        rating = request.form["rating"]
        club_id = request.form["club_id"]

        name = name[:255]
        gender = gender[:20]
        contact = contact[:20]

        conexao = conexao_db()
        cursor = conexao.cursor()  # Executa os comandos

        # Verifica se o jogador já existe
        cursor.execute(
            '''SELECT COUNT(*) FROM players WHERE name = %s''', (name,))
        exists = cursor.fetchone()[0]

        if exists > 0:
            # Jogador já existe, você pode retornar uma mensagem ou redirecionar
            cursor.close()
            conexao.close()
            return render_template("add_player.html", clubs=selecionar_clubes(), error="Jogador já cadastrado!")

        cursor.execute('''INSERT INTO players (name, birthdate, gender, contact, rating, club_id) VALUES (%s, %s, %s, %s, %s, %s)''',
                       (name, birthdate, gender, contact, rating, club_id))  # executa SQL
        conexao.commit()

        cursor.close()  # fechao o cursor
        conexao.close()  # fecha a conexão

        print("Dados cadastrados!")
        # renderiza o template HTML e retorna para o index.html
        return redirect(url_for('players.add_player'))

    else:
        clubes = selecionar_clubes()
        return render_template("add_player.html", clubs=clubes)


# GET: solicita dados do servidor
@players_blueprint.route("/list_players", methods=["GET"])
@login_required
def list_players():
    """Lista os jogadores"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute('''SELECT players.id, players.name, players.birthdate, players.gender, players.contact, players.rating, clubs.name AS club_name
        FROM players
        LEFT JOIN clubs ON players.club_id = clubs.id
        WHERE players.status = 'Ativo' ''')
    data = cursor.fetchall()
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return render_template("list_players.html", players=data)


# GET: solicita dados do servidor
@players_blueprint.route("/edit_player/<int:id>", methods=["GET"])
@login_required
def edit_player(id):
    """Editar um jogador"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute('''SELECT * FROM players WHERE id = %s''', (id,))
    player = cursor.fetchone()

    cursor.execute('''SELECT id, name FROM clubs WHERE status = 'ativo' ''')
    clubes = cursor.fetchall()

    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return render_template("edit_player.html", player=player, clubs=clubes)


@players_blueprint.route("/update_player/<int:id>", methods=["POST"])
@login_required
def update_player(id):
    """Atualiza dados de um jogador"""
    if request.method == "POST":
        name = request.form["nome"]
        birthdate = request.form["data_nascimento"]
        gender = request.form["sexo"]
        contact = request.form["contato"]
        rating = request.form["rating"]
        club_id = request.form["club_id"]

        name = name[:255]
        gender = gender[:20]
        contact = contact[:20]

        conexao = conexao_db()
        cursor = conexao.cursor()  # Executa os comandos
        cursor.execute('''UPDATE players SET name = %s, birthdate = %s, gender = %s, contact = %s, rating = %s, club_id = %s WHERE id = %s
        ''', (name, birthdate, gender, contact, rating, club_id, id))  # executa SQL
        conexao.commit()

        cursor.close()  # fechao o cursor
        conexao.close()  # fecha a conexão

        return redirect(url_for('players.list_players'))

    else:
        def selecionar_clubes():
            conexao = conexao_db()
            cursor = conexao.cursor()
            cursor.execute(
                '''SELECT id, name FROM clubs WHERE status = 'ativo' ''')

            clubes = cursor.fetchall()
            cursor.close()
            conexao.close()
            return clubes
        clubes = selecionar_clubes()  # Chama a função para obter os clubes

        return render_template("edit_player.html", clubs=clubes)


@players_blueprint.route("/delete_player/<int:id>", methods=["POST"])
@login_required
def delete_player(id):
    """Deleta um jogador"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos

    cursor.execute(
        '''UPDATE players SET status = 'excluido' WHERE id = %s''', (id,))  # executa SQL
    conexao.commit()

    # Quando todos os clubes forem deletados o autoincrement reinicia
    cursor.execute("SELECT COUNT(*) FROM players")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("ALTER TABLE players AUTO_INCREMENT = 1")
        conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return redirect(url_for("players.list_players"))


@players_blueprint.route("/recover_player/<int:id>", methods=["POST"])
@login_required
def recover_player(id):
    """Restaura um jogador"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute(
        '''UPDATE players SET status = 'ativo' WHERE id = %s''', (id,))  # executa SQL
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return redirect(url_for("players.list_players_excluded"))


@players_blueprint.route("/list_players_excluded")
def list_players_excluded():
    """Liasta de jogadores excluídos"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos

    cursor.execute(
        '''SELECT id, name, birthdate, club_id FROM players WHERE status = 'excluído' ''')  # executa SQL
    players_excluded = cursor.fetchall()
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return render_template("list_players_excluded.html", players=players_excluded)


def selecionar_clubes():
    """Seleciona um clube"""
    conexao = conexao_db()
    cursor = conexao.cursor()
    cursor.execute('''SELECT id, name FROM clubs WHERE status = 'ativo' ''')
    clubes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return clubes


@players_blueprint.route("/check_player", methods=["POST"])
def check_player():
    """Verifica se o jogador já está cadastrado"""
    data = request.get_json()
    name = data["name"]

    conexao = conexao_db()
    cursor = conexao.cursor()

    cursor.execute('''SELECT COUNT(*) FROM players WHERE name = %s''', (name,))
    exists = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    return jsonify({"exists": exists > 0})
