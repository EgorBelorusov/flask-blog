from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


posts = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/posts')
def view_posts():
    return render_template("posts.html", posts=posts)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title") # сервер находит данные из текстового поля (input) по его имени name="title" и сохраняет их в переменную title
    text = request.form.get("text") # сервер находит данные из большого текстового поля (textarea) по его имени name="text" и сохраняет их в переменную text
    posts.insert(0, {'title': title, 'text': text}) # добавляем элемент на место индекса, метод списка

    return redirect(url_for("view_posts")) # перенаправляет на другой адрес, а url_for выполняет функцию в скобках и перенаправляет по её адресу




if __name__ == "__main__":
    app.run(debug=True)












