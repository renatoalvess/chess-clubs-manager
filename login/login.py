from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from db.models import User, conexao_db


login_blueprint = Blueprint('login', __name__, template_folder='templates')


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # Se o admin estiver logado, impede que outro usuário faça login sem antes deslogar
    if current_user.is_authenticated and current_user.is_admin:
        # flash("Você já está logado como administrador. Saia antes de entrar com outro usuário.", "info")
        return redirect(url_for("register.register"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Conecta ao banco de dados e verifica as credenciais
        conexao = conexao_db()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        conexao.close()

        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data["id"], user_data["username"],
                        user_data["password"], user_data.get("is_admin", False))

            # Se já houver um usuário logado, ele será deslogado antes do novo login
            if current_user.is_authenticated:
                logout_user()

            login_user(user)

            # Se for admin, redireciona para a área de administração
            if user.is_admin:
                return redirect(url_for("players.index"))
            return redirect(url_for("players.index"))
        else:
            flash("Usuário ou senha incorretos.", "error")

    return render_template("login.html")


@login_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("players.index"))


def load_user(user_id):
    conexao = conexao_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conexao.close()
    if user_data:
        return User(user_data["id"], user_data["username"], user_data["password"], user_data.get("is_admin", False))
    return None
