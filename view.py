# view.py

from telebot import types

class ExpenseView:
    @staticmethod
    def main_menu():
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton("Додати витрати")
        btn2 = types.KeyboardButton("Список витрат")
        btn3 = types.KeyboardButton("Редагувати витрати")
        markup.add(btn1, btn2)
        markup.add(btn3)
        return markup

    @staticmethod
    def prompt_for_amount():
        return "Введіть суму витрат:"

    @staticmethod
    def prompt_for_description():
        return "Введіть опис витрати:"

    @staticmethod
    def display_expenses(expenses):
        if not expenses:
            return "У вас немає витрат."
        message = "Ваші витрати:\n"
        for expense in expenses:
            message += f"ID: {expense[0]}, Сума: {expense[1]}, Опис: {expense[2]}, Дата: {expense[3]}\n"
        return message

    @staticmethod
    def expense_added():
        return "Витрату додано успішно!"

    @staticmethod
    def prompt_for_edit():
        return "Введіть ID витрати, яку бажаєте редагувати або видалити:"

    @staticmethod
    def prompt_edit_choice():
        return "Виберіть, що бажаєте змінити: Сума, Опис або Видалити."

    @staticmethod
    def prompt_for_new_amount():
        return "Введіть нову суму витрати:"

    @staticmethod
    def prompt_for_new_description():
        return "Введіть новий опис витрати:"

    @staticmethod
    def prompt_delete_expense_confirmation():
        return "Ви впевнені, що хочете видалити цю витрату? Введіть 'Так' для підтвердження."

    @staticmethod
    def expense_updated():
        return "Витрата успішно оновлена!"

    @staticmethod
    def expense_deleted():
        return "Витрату успішно видалено."
