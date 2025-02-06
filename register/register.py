from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from db.db import conexao_db

register_blueprint = Blueprint(
    'register', __name__, template_folder='templates')


@register_blueprint.route("/register", methods=["GET", "POST"])
@login_required  # Garante que apenas usuários logados possam acessar
def register():
    if not current_user.is_admin:
        flash("Você não tem permissão para acessar esta página.", "error")
        # Redireciona para uma página apropriada
        return redirect(url_for("login.login"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conexao = conexao_db()
        cursor = conexao.cursor()

        # Verifica se já existe um administrador
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # O primeiro usuário será admin
        is_admin = True if total_users == 0 else False

        # Criptografa a senha
        hashed_password = generate_password_hash(password)

        # Insere o usuário no banco
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)",
                       (username, hashed_password, is_admin))

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Usuário registrado com sucesso!", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")


# GET servidor envia dados
@register_blueprint.route("/list_users", methods=["GET"])
@login_required
def list_users():
    """Lista todos os usuários"""
    conexao = conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos
    cursor.execute('''SELECT * FROM users ''')  # executa SQL
    data = cursor.fetchall()
    conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return render_template("list_users.html", users=data)


@register_blueprint.route("/delete_users/<int:id>", methods=["POST"])
def delete_user(id):
    """Deleta um usuário"""
    if not current_user.is_admin:
        # flash("Você não tem permissão para acessar esta página.", "error")
        return redirect(url_for("login.login"))

    conexao = conexao_db()
    cursor = conexao.cursor()  # Executa os comandos

    cursor.execute('''DELETE FROM users WHERE id = %s''', (id,))
    conexao.commit()

    # Quando todos os usuaários forem deletados, o autoincrement reinicia.
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")
        conexao.commit()

    cursor.close()  # fechao o cursor
    conexao.close()  # fecha a conexão

    return redirect(url_for("register.list_users"))


@register_blueprint.route("/edit_user/<int:id>", methods=["GET"])
def edit_user(id):
    """Edita um usuário"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            conexao = conexao_db()
            cursor = conexao.cursor()  # Executa os comandos
            cursor.execute('''SELECT * FROM users WHERE id=%s''', (id,))
            user = cursor.fetchone()
            conexao.commit()

            cursor.close()  # fechao o cursor
            conexao.close()  # fecha a conexão

            return render_template("edit_user.html", user=user)
    return redirect(url_for("login.login"))


@register_blueprint.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):
    """Atualiza um usuário"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            username = request.form["nome"]
            password = request.form["senha"]

            username = username[:50]
            password = password[:255]

            conexao = conexao_db()
            cursor = conexao.cursor()  # Executa os comandos

            if password:
                # Criptografa a senha antes de salvar no banco
                hashed_password = generate_password_hash(password)
                cursor.execute(
                    '''UPDATE users SET username = %s, password = %s WHERE id = %s''', (username, hashed_password, id))
            else:
                cursor.execute(
                    '''UPDATE users SET username = %s WHERE id = %s''', (username, id))

            conexao.commit()
            cursor.close()
            conexao.close()

            return redirect(url_for("register.list_users"))
    return redirect(url_for("register.list_user"))
