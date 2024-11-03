import sqlite3

class ExpenseModel:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_expense(self, user_id, amount, description):
        self.cursor.execute('''
            INSERT INTO expenses (user_id, amount, description)
            VALUES (?, ?, ?)
        ''', (user_id, amount, description))
        self.conn.commit()

    def get_expenses(self, user_id):
        self.cursor.execute('''
            SELECT id, amount, description, date
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (user_id,))
        return self.cursor.fetchall()

    def delete_expense(self, expense_id):
        self.cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        self.conn.commit()

    def update_expense_amount(self, expense_id, new_amount):
        self.cursor.execute('''
            UPDATE expenses
            SET amount = ?
            WHERE id = ?
        ''', (new_amount, expense_id))
        self.conn.commit()

    def update_expense_description(self, expense_id, new_description):
        self.cursor.execute('''
            UPDATE expenses
            SET description = ?
            WHERE id = ?
        ''', (new_description, expense_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
