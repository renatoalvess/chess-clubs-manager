import mysql.connector
from flask import Blueprint, Flask, render_template, request, jsonify
from db.db import conexao_db


conexao = conexao_db()


ranking_blueprint = Blueprint('ranking', __name__, template_folder='templates')


@ranking_blueprint.route('/ranking', methods=['GET'])
def ranking():
    conexao = conexao_db()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, name FROM clubs WHERE status = 'Ativo'")
    clubs = cursor.fetchall()

    # Obter o ID do clube selecionado a partir dos parâmetros da URL
    club_id = request.args.get('club', '')

    # Query para filtrar os jogadores por clube ou exibir todos
    if club_id:
        query = '''SELECT players.id, players.name, players.rating, clubs.name AS club_name
                   FROM players
                   LEFT JOIN clubs ON players.club_id = clubs.id
                   WHERE players.status = 'Ativo' AND players.club_id = %s
                   ORDER BY players.rating DESC'''
        cursor.execute(query, (club_id,))
    else:
        query = '''SELECT players.id, players.name, players.rating, clubs.name AS club_name
                   FROM players
                   LEFT JOIN clubs ON players.club_id = clubs.id
                   WHERE players.status = 'Ativo'
                   ORDER BY players.rating DESC'''
        cursor.execute(query)

    players = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("ranking.html", players=players, clubs=clubs, request=request)
