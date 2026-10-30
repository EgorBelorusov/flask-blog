import sqlite3



def init_db():
    connection = sqlite3.connect("blog.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
    connection.commit()
    connection.close()

    return "Выполнено!"





def get_posts():
    connection = sqlite3.connect("blog.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    connection.close()
    return posts





def add_post(title, text):
    connection = sqlite3.connect("blog.db")
    cursor = connection.cursor()
    if title:
        cursor.execute("INSERT INTO posts (title, text) VALUES (?, ?)", (title, text))
        connection.commit()
    connection.close()

    return
