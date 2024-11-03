from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Ініціалізація бази даних з таблицею для автентифікованих користувачів
def init_db():
    conn = sqlite3.connect('auth_users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authenticated_users (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

# Маршрут для отримання даних після аутентифікації
@app.route('/')
def auth():
    user_id = request.args.get('id')
    if user_id:
        conn = sqlite3.connect('auth_users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO authenticated_users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        conn.close()
        return "Ви успішно аутентифіковані!", 200
    else:
        return "Помилка аутентифікації.", 400

if __name__ == '__main__':
    init_db()
    app.run(port=5000)