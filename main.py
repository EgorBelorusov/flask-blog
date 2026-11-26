from werkzeug.security import check_password_hash
from flask import Flask, request, render_template, redirect, url_for, session
from db import init_db, get_posts, add_post, delete_posts, add_users, get_user_by_email
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os




app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

if app.secret_key is None or not app.secret_key:
    raise RuntimeError("SECRET_KEY не задан в .env")


init_db()


@app.route("/")
def index():
    result = get_posts()
    return render_template("index.html", result=result)





@app.route("/register")
def registration():
    return render_template("register.html")





@app.route("/login")
def login():
    return render_template("login.html")





@app.route("/login", methods=["POST"])
def authenticate_user():
    user_email = request.form.get("user_email", "").strip().lower()
    user_password = request.form.get("user_password", "")

    if not user_email:
        return render_template("login.html", error="Введите почту", user_email=user_email)

    if not user_password:
        return render_template("login.html", error="Введите пароль", user_email=user_email)

    user = get_user_by_email(user_email)

    if user is None or not check_password_hash(user["password_hash"], user_password):
        return render_template("login.html", error="Неправильная почта или пароль", user_email=user_email)

    session.clear()
    session["user_id"] = user["id"]

    return redirect(url_for("index"))





@app.route('/register', methods=["POST"])
def register():
    surname = request.form.get("surname", "").strip()
    name = request.form.get("name", "").strip()
    patronymic = request.form.get("patronymic", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    password_repid = request.form.get("password_repid", "")
    password_hash = generate_password_hash(password)

    if password != password_repid:
        return render_template("register.html", error="Пароли не совпали", email=email, surname=surname, name=name, patronymic=patronymic)

    if len(password) < 8:
        return render_template("register.html", error="Пароль меньше 8 символов", email=email, surname=surname, name=name, patronymic=patronymic)

    if not surname:
        return render_template("register.html", error="Пустое поле 'Фамилия'", email=email, surname=surname, name=name, patronymic=patronymic)

    if not name:
        return render_template("register.html", error="Пустое поле 'Имя'", email=email, surname=surname, name=name, patronymic=patronymic)

    if not email:
        return render_template("register.html", error="Пустое поле 'Почта'", email=email, surname=surname, name=name, patronymic=patronymic)

    add = add_users(surname, name, patronymic, email, password_hash)

    if not add:
        return render_template("register.html", error="Почта занята", email=email, surname=surname, name=name, patronymic=patronymic)



    return redirect(url_for("index"))





@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip() # сервер находит данные из текстового поля (input) по его имени name="title" и сохраняет их в переменную title
    text = request.form.get("text", "").strip() # сервер находит данные из большого текстового поля (textarea) по его имени name="text" и сохраняет их в переменную text
    add_post(title, text)

    return redirect(url_for("index")) # перенаправляет на другой адрес, а url_for возвращает адрес который привязан к функции в скобках





@app.route("/delete/<int:post_id>", methods=["Post"])
def delete(post_id):
    delete_posts(post_id)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

