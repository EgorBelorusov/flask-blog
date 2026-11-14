import sqlite3

DB_NAME = "blog.db"

def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surname TEXT NOT NULL,
            name TEXT NOT NULL,
            patronymic TEXT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()






def get_posts():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()

    return posts



def get_users():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()

    return users





def add_post(title, text):
    if title:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO posts (title, text) VALUES (?, ?)", (title, text))
        connection.commit()
        connection.close()





def add_users(surname, name, patronymic, email, password_hash):
    connection = sqlite3.connect(DB_NAME)
    
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (surname, name, patronymic, email, password_hash) VALUES (?, ?, ?, ?, ?)", (surname, name, patronymic, email, password_hash))
        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()





def delete_posts(post_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()


