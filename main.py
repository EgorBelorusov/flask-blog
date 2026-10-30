from flask import Flask, request, render_template, redirect, url_for
from db import init_db, get_posts, add_post

app = Flask(__name__)

init_db()

@app.route("/")
def index():
    return render_template("index.html")





@app.route('/posts')
def view_posts():
    result = get_posts()
    return render_template("posts.html", result=result)





@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip() # сервер находит данные из текстового поля (input) по его имени name="title" и сохраняет их в переменную title
    text = request.form.get("text", "").strip() # сервер находит данные из большого текстового поля (textarea) по его имени name="text" и сохраняет их в переменную text
    add_post(title, text)

    return redirect(url_for("view_posts")) # перенаправляет на другой адрес, а url_for возвращает адрес который привязан к функции в скобках





if __name__ == "__main__":
    app.run(debug=True)

