import mysql.connector
from flask import Blueprint, Flask, render_template, request, jsonify
from flask_login import login_required
from db.db import conexao_db


conexao = conexao_db()


class Player:
    def __init__(self, id, name, rating):
        self.id = id
        self.name = name
        self.rating = rating

    @staticmethod
    def buscar_player(id):
        conexao = conexao_db()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM players WHERE id = %s", (id,))
        player_data = cursor.fetchone()
        cursor.close()
        conexao.close()

        if player_data:
            return Player(player_data['id'], player_data['name'], player_data['rating'])
        return None

    def atualizar_rating(self, novo_rating):
        conexao = conexao_db()
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE players SET rating = %s WHERE id = %s", (novo_rating, self.id))
        conexao.commit()
        cursor.close()
        conexao.close()
        self.rating = novo_rating


class Partida:
    def __init__(self, id, player1_id, player2_id, result, date=None):
        self.id = id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.result = result
        self.date = date

    @staticmethod
    def criar_partida(player1_id, player2_id, result, date=None):
        conexao = conexao_db()
        cursor = conexao.cursor()

        query = "INSERT INTO matches (player1_id, player2_id, result, date) VALUES (%s, %s, %s, %s)"
        # Certifique-se de passar a data aqui
        cursor.execute(query, (player1_id, player2_id, result, date))

        partida_id = cursor.lastrowid
        conexao.commit()

        cursor.close()
        conexao.close()

        return Partida(partida_id, player1_id, player2_id, result, date)

    def calcular_rating(self):
        jogador1 = Player.buscar_player(self.player1_id)
        jogador2 = Player.buscar_player(self.player2_id)

        K = 20
        R1 = 10 ** (jogador1.rating / 400)
        R2 = 10 ** (jogador2.rating / 400)

        E1 = R1 / (R1 + R2)

        novo_rating1 = round(jogador1.rating + K * (self.result - E1))
        novo_rating2 = round(jogador2.rating + K *
                             ((1 - self.result) - (1 - E1)))

        jogador1.atualizar_rating(novo_rating1)
        jogador2.atualizar_rating(novo_rating2)

        return novo_rating1, novo_rating2


rating_blueprint = Blueprint('rating', __name__, template_folder='templates')


@rating_blueprint.route("/")
def index():
    return render_template("index.html")


@rating_blueprint.route('/criar_partida', methods=['GET', 'POST'])
def criar_partida():
    if request.method == 'POST':
        player1_id = request.form.get('jogador1_id')
        player2_id = request.form.get('jogador2_id')
        result = request.form.get('result')
        date = request.form.get('date')  # Capturando a data do formulário

        # Verificar se os campos obrigatórios estão preenchidos
        if not player1_id or not player2_id or result is None or not date:
            return jsonify({"erro": "Dados incompletos no formulário"}), 400

        try:
            # Converter IDs para inteiros e resultado para float
            player1_id = int(player1_id)
            player2_id = int(player2_id)
            result = float(result)

            # Verificar se os jogadores existem no banco de dados
            if not Player.buscar_player(player1_id) or not Player.buscar_player(player2_id):
                return jsonify({"erro": "Um ou ambos os jogadores não existem."}), 404

            # Criar a partida e calcular os novos ratings
            partida = Partida.criar_partida(
                player1_id, player2_id, result, date)  # Passando a data aqui
            novo_rating1, novo_rating2 = partida.calcular_rating()

            # Renderizar a página com os resultados
            return render_template("criar_partida.html",
                                   partida_id=partida.id,
                                   novo_rating_jogador1=novo_rating1,
                                   novo_rating_jogador2=novo_rating2)

        except ValueError:
            return render_template("criar_partida.html", erro="IDs dos jogadores e resultado precisam ser números válidos")

    return render_template('criar_partida.html')


@rating_blueprint.route('/buscar_jogadores', methods=['GET'])
def buscar_jogadores():
    term = request.args.get('term', '')  # Captura o termo da query string
    conexao = conexao_db()
    cursor = conexao.cursor(dictionary=True)

    # Usar LIKE para filtrar jogadores que começam com o termo
    query = """
    SELECT p.id AS player_id, p.name AS player_name, p.rating
    FROM players AS p
    WHERE p.name LIKE %s
    """

    # Adiciona '%' para buscar por prefixo
    cursor.execute(query, (term + '%',))
    jogadores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify([
        {"label": jogador["player_name"],
            "value": jogador["player_id"], "rating": jogador["rating"]}
        for jogador in jogadores
    ])


# GET: solicita dados do servidor
@rating_blueprint.route("/list_matches", methods=["GET"])
def list_matches():
    """Lista de partidas"""
    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute('''SELECT m.id, p1.name AS player1_name, p2.name AS player2_name, date,
                   CASE 
                        WHEN m.result = 1 THEN '1 - 0' 
                        WHEN m.result = 0.5 THEN '½ - ½' 
                        WHEN m.result = 0 THEN '0 - 1' 
                        END AS formatted_result 
                   FROM 
                        matches m 
                   INNER JOIN players p1 ON m.player1_id = p1.id 
                   INNER JOIN players p2 ON m.player2_id = p2.id 
                   ORDER BY m.id
                   ''')  # executa SQL
    data = cursor.fetchall()
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return render_template("lista_partidas.html", matches=data)
