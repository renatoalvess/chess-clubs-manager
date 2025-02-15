from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import mysql.connector
from db.db import conexao_db


conexao = conexao_db()


notices_blueprint = Blueprint('notices', __name__, template_folder='templates')


@notices_blueprint.route('/adicionar_noticia', methods=['GET', 'POST'])
@login_required
def adicionar_noticia():
    if current_user.is_authenticated:  # Verifica se o usuário está logado
        if not current_user.is_admin:
            # flash("Você não tem permissão para acessar esta página.", "error")
            return redirect(url_for("login.login"))
    if request.method == 'POST':

        titulo = request.form['titulo']
        imagem_url = request.form['imagem_url']
        conteudo_html = request.form['conteudo_html']

        # Depuração: Verifique o valor do título
        print(f"Título a ser inserido: {titulo}")
        print(f"Tamanho do título: {len(titulo)}")

        conexao = conexao_db()
        cursor = conexao.cursor() 

        try:
            cursor.execute(
                'INSERT INTO notices (titulo, conteudo_html, imagem_url) VALUES (%s, %s, %s)',
                (titulo, conteudo_html, imagem_url)
            )
            conexao.commit()
            # flash('Notícia adicionada com sucesso!', 'success')
        except Exception as e:
            conexao.rollback()
            # flash(f'Erro ao adicionar notícia: {str(e)}', 'error')
        finally:
            cursor.close()
            conexao.close()
            

    return render_template('adicionar_noticia.html')

@notices_blueprint.route("/noticia/<int:id>")
def detalhes_noticia(id):
    conexao = conexao_db()
    cursor = conexao.cursor(dictionary=True)

    # Buscar a notícia pelo ID
    cursor.execute('''SELECT * FROM notices WHERE id = %s''', (id,))
    noticia = cursor.fetchone()

    # Buscar outras notícias para exibir na lateral
    cursor.execute('''SELECT * FROM notices WHERE id != %s ORDER BY data_publicacao DESC LIMIT 20''', (id,))
    outras_noticias = cursor.fetchall()

    cursor.close()
    conexao.close()

    if noticia:
        return render_template('detalhes_noticia.html', noticia=noticia, outras_noticias=outras_noticias)
    else:
        return "Notícia não encontrada.", 404
    
@notices_blueprint.route("/listar_noticias", methods=["GET"])
def listar_noticias():
    conexao = conexao_db()
    cursor = conexao.cursor(dictionary=True)

    # Buscar as últimas notícias
    cursor.execute('''SELECT * FROM notices ORDER BY data_publicacao DESC LIMIT 20''')
    noticias = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Renderizar a página com as notícias e a opção de deletar
    return render_template('listar_noticias.html', noticias=noticias)

@notices_blueprint.route("/noticia/deletar/<int:id>", methods=["POST"])
def deletar_noticia(id):
    conexao = conexao_db()
    cursor = conexao.cursor()

    # Deletar a notícia
    cursor.execute('''DELETE FROM notices WHERE id = %s''', (id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    # Redirecionar de volta para a lista de notícias após deletar
    return redirect(url_for('notices.listar_noticias'))

    
@notices_blueprint.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')

@notices_blueprint.route('/xadrez_escola', methods=['GET'])
def xadrez_escola():
    return render_template('xadrez_na_escola.html')

@notices_blueprint.route('/xadrez_logico', methods=['GET'])
def xadrez_logico():
    return render_template('xadrez_logico.html')
