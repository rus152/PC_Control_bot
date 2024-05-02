import telebot
from telebot import types
from tkinter import *
from tkinter import messagebox
import os
import re
import json
import random

debug_start = 0
debug_user_data = 0

""" Фигня для отладки """
if(debug_start == 1):
    try:
        os.remove(os.getenv('APPDATA') + '\PC_Control_Bot\\token')
    except:
        pass
    os.rmdir(os.getenv('APPDATA') + '\PC_Control_Bot')
    messagebox.showinfo("Успешно", "Токен был удалён")
    exit()

if(debug_user_data == 1):
    try:
        os.remove(os.getenv('APPDATA') + '\PC_Control_Bot\\Users.json')
    except:
        pass
    messagebox.showinfo("Успешно", "Данные пользователей удалены")
    exit()

""" Словарь """
user_data = {}
user_states = {}


def on_confirm():
    global user_input  # Глобальная переменная для хранения ввода пользователя
    user_input = enter_token.get() # Получаем текст из текстового поля

    """ Проверка валидности """

    if validate_token(user_input):
        messagebox.showinfo("Успешно", "Токен валиден")
        tkn_val = 1
    else:
        messagebox.showerror("Ошибка", "Невалидный токен")
        tkn_val = 0

    """ Вписывания в APPDATA токена, для последующего использования """

    if (tkn_val == 1):
        try:
            os.mkdir(os.getenv('APPDATA') + '\PC_Control_Bot')
        except:
            pass
        f = open(os.getenv('APPDATA') + '\PC_Control_Bot\\token', 'w')
        f.write(user_input)
        f.close()
        window.destroy()
    else:
        pass

def validate_token(token):
    """ Проверка токена с помощью регулярного выражения и длины. """
    pattern = re.compile(r"^\d{10}:.+$")  # Первые 10 символов - цифры, затем двоеточие и любые символы
    return pattern.match(token) is not None and len(token) == 46

def on_exit():
    exit()

def login_system(user_id):
    if user_id in banned_users:
        return "ban"
    elif user_id in verified_users:
        return "val"
    else:
        pass


def generate_code():
    return random.randint(100000, 999999)

def get_user_state(user_id):
    return user_states.get(user_id, None)

def set_user_state(user_id, state):
    user_states[user_id] = state

""" Проверка существования токена в APPDATA и создание его при отсутствии """

try:
    f = open(os.getenv('APPDATA') + '\PC_Control_Bot\\token', 'r')
    f.close()
except (IOError) and (Exception):
    window = Tk()
    window.title("Тест окно")

    lbl = Label(window, text="Введите свой Токен")
    lbl.grid(column=0, row=0)

    enter_token = Entry(window)
    enter_token.grid(column=0, row=1)

    confirm_button = Button(window, text="Подтвердить", command=on_confirm)
    confirm_button.grid(column=0, row=2)

    exit_button = Button(window, text="Выйти", command=on_exit)
    exit_button.grid(column=1, row=2)

    window.mainloop()

"""Проверка и загрузка списока пользователей"""

if not os.path.exists(os.getenv('APPDATA') + '\PC_Control_Bot\\Users.json'):
    with open(os.getenv('APPDATA') + '\PC_Control_Bot\\Users.json', 'w') as file:
        json.dump({"verified": [], "banned": []}, file)

with open(os.getenv('APPDATA') + '\PC_Control_Bot\\Users.json') as file:
    data = json.load(file)

verified_users = set(data['verified'])
banned_users = set(data['banned'])

def save_data():
    with open(os.getenv('APPDATA') + '\PC_Control_Bot\\Users.json', 'w') as file:
        json.dump({"verified": list(verified_users), "banned": list(banned_users)}, file)


token_code = open(os.getenv('APPDATA') + '\PC_Control_Bot\\token', 'r')
token = token_code.read()
token_code.close()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'], func=lambda message: get_user_state(message.chat.id) == None)
def send_welcome(message):
    user_id = message.from_user.id
    if login_system(user_id) == "val":
        bot.send_message(message.chat.id, f'Не стоит {message.from_user.first_name}. Вы уже ве')
    elif login_system(user_id) == "ban":
        print("Кто ты?")
    else:
        print("Я тебя не знаю")


@bot.message_handler(commands=['ver'], func=lambda message: get_user_state(message.chat.id) == None)
def send_welcome(message):
    user_id = message.from_user.id
    if login_system(user_id) == "val":
        bot.send_message(message.chat.id, f'Не стоит {message.from_user.first_name}. Вы уже верифицированы')
    elif login_system(user_id) == "ban":
        bot.send_message(message.chat.id, f'Вы уже заблокированы')
    else:
        chat_id = message.chat.id
        user_data[chat_id] = generate_code()
        print("Используйте этот код для проверки:", user_data[chat_id])
        bot.send_message(message.chat.id, f'Вам в консоли вывелись числа для верификации, пожалуйста, введите их сюда для верификации акаунта')
        set_user_state(user_id, 'waiting_for_code')

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == 'waiting_for_code')
def check_code(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        user_code = int(message.text)
        if chat_id in user_data and user_data[chat_id] == user_code:
            bot.reply_to(message, "Код валиден! Вы теперь верифицированы.")
            verified_users.add(user_id)
            save_data()
            set_user_state(user_id, None)
        else:
            bot.reply_to(message, "Код не валиден. Вы заблокированы.")
            banned_users.add(user_id)
            save_data()
            set_user_state(user_id, None)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите 6-значный числовой код.")

bot.polling(none_stop=True)

