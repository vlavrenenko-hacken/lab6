import telebot
from model import ExpenseModel
from view import ExpenseView
import sqlite3

bot = telebot.TeleBot("TELEGRAM_TOKEN") 
model = ExpenseModel()

# Перевірка аyтентифікації користувача
def is_authenticated(user_id):
    conn = sqlite3.connect('auth_users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM authenticated_users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Запуск через /start або /help
@bot.message_handler(commands=['start', 'help'])
def start(message):
    user_id = message.from_user.id
    if is_authenticated(user_id):
        bot.send_message(message.chat.id, "Вітаю, оберіть функцію", reply_markup=ExpenseView.main_menu())
    else:
        bot.send_message(message.chat.id, "Ви не авторизовані для використання цього бота. Пройдіть аутентифікацію через веб-сайт.")

# Функція для додавання нової витрати
@bot.message_handler(func=lambda message: message.text == "Додати витрати")
def add_expense(message):
    user_id = message.from_user.id
    if is_authenticated(user_id):
        bot.send_message(message.chat.id, ExpenseView.prompt_for_amount())
        bot.register_next_step_handler(message, process_amount)
    else:
        bot.send_message(message.chat.id, "Ви не авторизовані для використання цієї функції.")

# Функція для обробки суми та запиту опису
def process_amount(message):
    try:
        amount = float(message.text)
        bot.send_message(message.chat.id, ExpenseView.prompt_for_description())
        bot.register_next_step_handler(message, lambda msg: process_description(msg, amount))
    except ValueError:
        bot.send_message(message.chat.id, "Введіть дійсне число.")

# Функція для додавання опису та збереження запису
def process_description(message, amount):
    description = message.text
    user_id = message.from_user.id
    if is_authenticated(user_id):
        model.add_expense(user_id, amount, description)
        bot.send_message(message.chat.id, ExpenseView.expense_added())
    else:
        bot.send_message(message.chat.id, "Ви не авторизовані для використання цієї функції.")

# Функція для показу списку витрат
@bot.message_handler(func=lambda message: message.text == "Список витрат")
def list_expenses(message):
    user_id = message.from_user.id
    if is_authenticated(user_id):
        expenses = model.get_expenses(user_id)
        bot.send_message(message.chat.id, ExpenseView.display_expenses(expenses))
    else:
        bot.send_message(message.chat.id, "Ви не авторизовані для використання цієї функції.")

# Функція для редагування витрат
@bot.message_handler(func=lambda message: message.text == "Редагувати витрати")
def edit_expense(message):
    user_id = message.from_user.id
    if is_authenticated(user_id):
        expenses = model.get_expenses(user_id)
        if expenses:
            bot.send_message(message.chat.id, ExpenseView.display_expenses(expenses) + "\n" + ExpenseView.prompt_for_edit())
            bot.register_next_step_handler(message, process_edit_choice)
        else:
            bot.send_message(message.chat.id, "У вас немає витрат для редагування.")
    else:
        bot.send_message(message.chat.id, "Ви не авторизовані для використання цієї функції.")

# Функції редагування та видалення витрати
def process_edit_choice(message):
    try:
        global editing_expense_id
        editing_expense_id = int(message.text)
        bot.send_message(message.chat.id, ExpenseView.prompt_edit_choice())
        bot.register_next_step_handler(message, handle_edit_choice)
    except ValueError:
        bot.send_message(message.chat.id, "Введіть дійсний ID витрати.")

def handle_edit_choice(message):
    choice = message.text.lower()
    if choice == "сума":
        bot.send_message(message.chat.id, ExpenseView.prompt_for_new_amount())
        bot.register_next_step_handler(message, update_amount)
    elif choice == "опис":
        bot.send_message(message.chat.id, ExpenseView.prompt_for_new_description())
        bot.register_next_step_handler(message, update_description)
    elif choice == "видалити":
        bot.send_message(message.chat.id, ExpenseView.prompt_delete_expense_confirmation())
        bot.register_next_step_handler(message, confirm_delete_expense)
    else:
        bot.send_message(message.chat.id, "Будь ласка, введіть 'Сума', 'Опис' або 'Видалити'.")

def update_amount(message):
    try:
        new_amount = float(message.text)
        model.update_expense_amount(editing_expense_id, new_amount)
        bot.send_message(message.chat.id, ExpenseView.expense_updated())
    except ValueError:
        bot.send_message(message.chat.id, "Введіть дійсне число.")

def update_description(message):
    new_description = message.text
    model.update_expense_description(editing_expense_id, new_description)
    bot.send_message(message.chat.id, ExpenseView.expense_updated())

def confirm_delete_expense(message):
    if message.text.lower() == "так":
        model.delete_expense(editing_expense_id)
        bot.send_message(message.chat.id, ExpenseView.expense_deleted())
    else:
        bot.send_message(message.chat.id, "Видалення скасовано.")


bot.polling(none_stop=True)
