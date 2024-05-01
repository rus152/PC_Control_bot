import telebot
from telebot import types
from tkinter import *
from tkinter import messagebox
import os
import re

debug_start = 0

tkn_val = 0

def on_confirm():
    global user_input  # Глобальная переменная для хранения ввода пользователя
    user_input = enter_token.get() # Получаем текст из текстового поля
    print(user_input)
    if validate_token(user_input):
        messagebox.showinfo("Успешно", "Токен валиден")
        tkn_val = 1
    else:
        messagebox.showerror("Ошибка", "Невалидный токен")
        tkn_val = 0

    if (tkn_val == 1):
        os.mkdir(os.getenv('APPDATA') + '\PC_Control_Bot')
        f = open(os.getenv('APPDATA') + '\PC_Control_Bot\\token', 'w')
        f.write(user_input)
        f.close()
        window.destroy()
    else:
        pass

def validate_token(token):
    """ Проверка токена с помощью регулярного выражения и длины. """
    pattern = re.compile(r"^\d{10}:.+$")  # Первые 10 символов - цифры, затем двоеточие и любое количество символов
    return pattern.match(token) is not None and len(token) == 46

def on_exit():
    exit()

if(debug_start == 1):
    os.rmdir(os.getenv('APPDATA') + '\PC_Control_Bot')
    exit()


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



token = "5169915860:AAFbTMdwuktxXRvpTzZdLqDOVHtrjUP8X5Y"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Айм элайв')

bot.polling(none_stop=True)

