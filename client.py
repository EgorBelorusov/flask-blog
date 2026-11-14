import requests
r = requests.post("http://127.0.0.1:5000/register",
                  data={"surname": "", "name": "Иван", "email": "a@a.ru",
                        "password": "12345678", "password_repid": "12345678"})
print(r.status_code, "Пустое поле" in r.text)


import sqlite3
conn = sqlite3.connect("blog.db")
print(conn.execute("SELECT id, email, password_hash FROM users").fetchall())
conn.close()