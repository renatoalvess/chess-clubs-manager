from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from flask_login import login_required, current_user
from db.db import conexao_db

import mysql.connector

clubs_blueprint = Blueprint('clubs', __name__, template_folder='templates')


@clubs_blueprint.route("/")  # Rota raiz
def index():
    conexao = conexao_db()
    cursor = conexao.cursor()

    # Consulta para buscar o total de clubes ativos
    cursor.execute("SELECT COUNT(*) FROM clubs WHERE status = 'ativo'")
    total_clubes = cursor.fetchone()[0]

    # Consulta para buscar o total de jogadores ativos
    cursor.execute("SELECT COUNT(*) FROM players WHERE status = 'Ativo'")
    total_jogadores = cursor.fetchone()[0]

    # Consulta para buscar o total de partidas
    cursor.execute("SELECT COUNT(*) FROM matches")
    total_partidas = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM notices ORDER BY data_publicacao DESC")
    todas_noticias = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    cursor.close()
    conexao.close()

    # Define os limites
    limite_cards = 4
    limite_notices = 2

    # Separa as notícias para cards e notices usando os limites
    cards_noticias = todas_noticias[:limite_cards]  # Cards: 4 primeiras notícias

    # Notices: 2 notícias a partir da 5ª posição (índice 4)
    notices_noticias = todas_noticias[limite_cards:limite_cards + limite_notices]

    # Renderizar o template com todos os valores buscados
    return render_template(
        'index.html',
        total_clubes=total_clubes,
        total_jogadores=total_jogadores,
        total_partidas=total_partidas,
        cards_noticias=cards_noticias,
        notices_noticias=notices_noticias,
        username=current_user.username if current_user.is_authenticated else None
    )



# rota add_club/aceita POST e GET. (POST: envia dados p/ servidor e GET: solicitado dados do servidor)
@clubs_blueprint.route("/add_club", methods=["POST", "GET"])
def add_club():
    """Cadastra um novo clube"""
    if request.method == "POST":
        # obtém o valor do campo de formulário com o nome "nome".
        name = request.form["nome"]
        # obtém o valor do campo de formulário com o nome "data_criacao".
        creation_date = request.form["data_criacao"]

        name = name[:255]

        conexao = conexao_db()
        cursor = conexao.cursor()  # Executa os comandos
        cursor.execute('''INSERT INTO clubs (name, creation_date) VALUES (%s, %s)''',
                       (name, creation_date))  # executa SQL
        conexao.commit()

        cursor.close()  # fechao o cursor
        conexao.close()  # fecha a conexão

        print("Dados cadastrados!")

    # renderiza o template HTML add_club.html
    return render_template("add_club.html")


# GET servidor envia dados
@clubs_blueprint.route("/list_clubs", methods=["GET"])
def list_clubs():
    """Lista todos os clubes"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute(
        '''SELECT * FROM clubs WHERE status = 'ativo' ''')  # executa SQL
    data = cursor.fetchall()
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return render_template("list_clubs.html", clubs=data)


@clubs_blueprint.route("/edit_club/<int:id>", methods=["GET"])
@login_required
def edit_club(id):
    """Exibe dados de um clube"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute('''SELECT * FROM clubs WHERE id=%s''', (id,))
    club = cursor.fetchone()
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return render_template("edit_club.html", club=club)


@clubs_blueprint.route("/update_club/<int:id>", methods=["POST"])
@login_required
def update_club(id):
    """Atualiza dados de um clube"""
    name = request.form["nome"]
    creation_date = request.form["data_criacao"]

    name = name[:255]

    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute('''UPDATE clubs SET name = %s, creation_date = %s WHERE id = %s''',
                   (name, creation_date, id))  # executa SQL
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return redirect(url_for("clubs.list_clubs"))


@clubs_blueprint.route("/delete_club/<int:id>", methods=["POST"])
@login_required
def delete_club(id):
    """Deleta um clube"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    # Atualiza os jogadores associados ao clube para NULL
    cursor.execute(
        '''UPDATE players SET club_id = NULL WHERE club_id = %s''', (id,))

    # Agora exclui o clube
    cursor.execute(
        '''UPDATE clubs SET status = 'Excluído' WHERE id = %s''', (id,))
    conexao.commit()

    # Quando todos os clubes forem deletados, o autoincrement reinicia
    cursor.execute("SELECT COUNT(*) FROM clubs WHERE status = 'Ativo'")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("ALTER TABLE clubs AUTO_INCREMENT = 1")
        conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return redirect(url_for("clubs.list_clubs"))


@clubs_blueprint.route("/recover_club/<int:id>", methods=["POST"])
@login_required
def recover_club(id):
    """Recupera um clube"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute(
        '''UPDATE clubs SET status = 'ativo' WHERE id = %s''', (id,))  # executa SQL
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return redirect(url_for("clubs.list_clubs_excluded"))


@clubs_blueprint.route("/list_clubs_excluded")
def list_clubs_excluded():
    """Lista os clubes excluídos"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute(
        '''SELECT id, name, creation_date FROM clubs WHERE status = 'excluído' ''')  # executa SQL
    clubs_excluded = cursor.fetchall()
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return render_template("list_clubs_excluded.html", clubs=clubs_excluded)


@clubs_blueprint.route("/check_club", methods=["POST"])
def check_club():
    """Verifica se o clube já está cadastrado"""
    data = request.get_json()
    name = data["name"]

    conexao = conexao_db()
    cursor = conexao.cursor()

    cursor.execute('''SELECT COUNT(*) FROM clubs WHERE name = %s''', (name,))
    exists = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    return jsonify({"exists": exists > 0})
