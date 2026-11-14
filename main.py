from flask import Flask, request, render_template, redirect, url_for
from db import init_db, get_posts, add_post, delete_posts, add_users, get_users
from werkzeug.security import generate_password_hash

app = Flask(__name__)

init_db()

@app.route("/")
def index():
    return render_template("index.html")





@app.route('/posts')
def view_posts():
    result = get_posts()
    return render_template("posts.html", result=result)




@app.route("/register")
def registration():
    return render_template("register.html")




@app.route("/users")
def view_users():
    users = get_users()
    return render_template("users.html", users=users)




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
        return render_template("register.html", error="Пароли не совпали", email=email, surname=surname, name=name)

    if len(password) < 8:
        return render_template("register.html", error="Пароль меньше 8 символов", email=email, surname=surname, name=name)

    if not surname:
        return render_template("register.html", error="Пустое поле 'Фамилия'", email=email, surname=surname, name=name)

    if not name:
        return render_template("register.html", error="Пустое поле 'Имя'", email=email, surname=surname, name=name)

    if not email:
        return render_template("register.html", error="Пустое поле 'Почта'", email=email, surname=surname, name=name)

    add = add_users(surname, name, patronymic, email, password_hash)

    if not add:
        return render_template("register.html", error="Почта занята", email=email, surname=surname, name=name)



    return redirect(url_for("index"))



@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip() # сервер находит данные из текстового поля (input) по его имени name="title" и сохраняет их в переменную title
    text = request.form.get("text", "").strip() # сервер находит данные из большого текстового поля (textarea) по его имени name="text" и сохраняет их в переменную text
    add_post(title, text)

    return redirect(url_for("view_posts")) # перенаправляет на другой адрес, а url_for возвращает адрес который привязан к функции в скобках




@app.route("/delete/<int:post_id>", methods=["Post"])
def delete(post_id):
    delete_posts(post_id)

    return redirect(url_for("view_posts"))


if __name__ == "__main__":
    app.run(debug=True)

