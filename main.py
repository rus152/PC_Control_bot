from tkinter import *
from tkinter import messagebox
import os
import re
import json
import random
import threading
import sys
import time
import requests

import telebot
from telebot import types
from notifypy import Notify
import pystray
from PIL import Image
from PIL import ImageGrab

###############
#   ОТЛАДКА   #
###############
debug = 1



###############
#   СЛОВАРИ   #
###############

user_data = {}
user_states = {}

########################
#   Основные функции   #
########################

def on_confirm():
    global user_input
    user_input = enter_token.get()

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
            os.mkdir(os.getenv('APPDATA') + '\\PC_Control_Bot')
        except:
            pass
        f = open(os.getenv('APPDATA') + '\\PC_Control_Bot\\token', 'w')
        f.write(user_input)
        f.close()
        window.destroy()
    else:
        pass

def validate_token(token):
    """ Проверка токена с помощью регулярного выражения и длины. """
    pattern = re.compile(r"^\d{10}:.+$")
    return pattern.match(token) is not None and len(token) == 46

def on_exit():
    os._exit(0)

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

def save_data():
    with open(os.getenv('APPDATA') + '\\PC_Control_Bot\\Users.json', 'w') as file:
        json.dump({"verified": list(verified_users), "banned": list(banned_users)}, file)

def code_display(chat_id, name):
    window = Tk()
    window.title("Верификации")
    window.iconbitmap(resource_path("icon.ico"))

    window.geometry("250x90")
    window.resizable(False, False)

    frame = Frame(window, bd=0)

    lbl0 = Label(window, text=f'Код для верификации аккаунта:\n{name}')
    lbl0.pack(pady=(0, 0))

    for i in range(6):
        lbl1 = Label(frame, text=f'{str(user_data[chat_id])[i]}')
        lbl1.grid(row=1, column=i)

    frame.place(relx=0.5, rely=0.5, anchor='center')

    window.mainloop()

def get_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Создание клавиатуры быстрого ввода
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("/shutdown")
    but2 = types.KeyboardButton("/ping")
    but3 = types.KeyboardButton("/hibernation")
    but5 = types.KeyboardButton("/screenshot")
    but6 = types.KeyboardButton("/lock")
    but4 = types.KeyboardButton("/cancel")
    markup.add(but1, but2, but3, but5, but6, but4)
    return markup

def time_select1(message):
    txt = message.text
    user_id = message.from_user.id

    if txt == "Назад":
        markup = get_keyboard()
        bot.reply_to(message, "Выход", parse_mode='html', reply_markup=markup)
        set_user_state(user_id, None)

    elif txt == "Часы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Отмена")
        markup.add(but1)
        bot.reply_to(message, "Через сколько часов?", parse_mode='html', reply_markup=markup)
        set_user_state(user_id, "Expectation_Hour")
        bot.register_next_step_handler(message, time_hour)

    elif txt == "Минуты":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Отмена")
        markup.add(but1)
        bot.reply_to(message, "Через сколько минут?", parse_mode='html', reply_markup=markup)
        set_user_state(user_id, "Expectation_Minute")
        bot.register_next_step_handler(message, time_Minute)

    elif txt == "Секунды":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Отмена")
        markup.add(but1)
        bot.reply_to(message, "Через сколько секунд?", parse_mode='html', reply_markup=markup)
        set_user_state(user_id, "Expectation_Second")
        bot.register_next_step_handler(message, time_Second)

    else:
        markup = get_keyboard()
        bot.reply_to(message, "Отмена", parse_mode='html', reply_markup=markup)
        set_user_state(user_id, None)


def time_hour(message):
    user_id = message.from_user.id
    time = message.text
    markup = get_keyboard()
    if time == "Отмена":
        bot.reply_to(message, "Возврат", parse_mode='html', reply_markup=markup)
        set_user_state(user_id, None)
        return
    else:
        try:
            os.system(f'shutdown /s /t {int(time) * 3600}')
            bot.reply_to(message, time_message(int(time) * 3600), parse_mode='html', reply_markup=markup)
            set_user_state(user_id, None)
            return
        except:
            bot.reply_to(message, 'Ошибка, отмена', parse_mode='html', reply_markup=markup)
            set_user_state(user_id, None)
            return

def time_Minute(message):
    user_id = message.from_user.id
    time = message.text
    markup = get_keyboard()
    if time == "Отмена":
        bot.reply_to(message, "Возврат", parse_mode='html', reply_markup=markup)
        set_user_state(user_id, None)
        return
    else:
        try:
            os.system(f'shutdown /s /t {int(time) * 60}')
            bot.reply_to(message, time_message(int(time) * 60), parse_mode='html', reply_markup=markup)
            set_user_state(user_id, None)
            return
        except:
            bot.reply_to(message, 'Ошибка, отмена',  parse_mode='html', reply_markup=markup)
            set_user_state(user_id, None)
            return

def time_Second(message):
    user_id = message.from_user.id
    time = message.text
    markup = get_keyboard()
    if time == "Отмена":
        bot.reply_to(message, "Возврат", parse_mode='html', reply_markup=markup)
        set_user_state(user_id, None)
        return
    else:
        try:
            os.system(f'shutdown /s /t {int(time)}')
            bot.reply_to(message, time_message(int(time)), parse_mode='html', reply_markup=markup)
            set_user_state(user_id, None)
            return
        except:
            bot.reply_to(message, 'Ошибка, отмена', parse_mode='html', reply_markup=markup)
            set_user_state(user_id, None)
            return

def time_message(seconds):
    if seconds >= 3600:
        hours = seconds / 3600
        unit = "час" if hours < 2 else "часа" if hours < 5 else "часов"
        return f"Компьютер отключится через {round(hours)} {unit} 🕑"
    elif seconds >= 60:
        minutes = seconds / 60
        unit = "минуту" if minutes < 2 else "минуты" if minutes < 5 else "минут"
        return f"Компьютер отключится через {round(minutes)} {unit} 🕑"
    elif seconds > 0:
        unit = "секунду" if seconds < 2 else "Секунды" if seconds < 5 else "секунд"
        return f"Компьютер отключится через {seconds} {unit} 🕑"
    else:
        return "Компьютер отключается"

def on_clicked_trei(icon, item):
    if str(item) == "Отчистка токена":
        os.remove(os.getenv('APPDATA') + '\\PC_Control_Bot\\token')
        messagebox.showinfo("Успешно", "Токен был удалён. Перезапуск")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    elif str(item) == "Отчистка Юзера":
        os.remove(os.getenv('APPDATA') + '\\PC_Control_Bot\\Users.json')
        messagebox.showinfo("Успешно", "Данные пользователей удалены. Перезапуск")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    elif str(item) == "Полный сброс":
        os.remove(os.getenv('APPDATA') + '\\PC_Control_Bot\\token')
        os.remove(os.getenv('APPDATA') + '\\PC_Control_Bot\\Users.json')
        os.rmdir(os.getenv('APPDATA') + '\\PC_Control_Bot')
        messagebox.showinfo("Успешно", "Папка удалена. Перезапуск")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    elif str(item) == "Перезагрузить":
        python = sys.executable
        os.execl(python, python, *sys.argv)
    elif str(item) == "Выход":
        icon.stop()
        try:
            os._exit(0)
        except SystemExit:
            print("Exiting...")

def trei():
    image = Image.open(resource_path("logo_init.png"))
    if debug == 1:
        icon = pystray.Icon('PC Control Bot', image, menu=pystray.Menu(
            pystray.MenuItem('Debug', pystray.Menu(
                             pystray.MenuItem("Перезагрузить", on_clicked_trei),
                             pystray.MenuItem("Отчистка токена", on_clicked_trei),
                             pystray.MenuItem("Отчистка Юзера", on_clicked_trei),
                             pystray.MenuItem("Полный сброс", on_clicked_trei)
                             )),
            pystray.MenuItem("Выход", on_clicked_trei)
        ))
    else:
        icon = pystray.Icon('PC Control Bot', image, menu=pystray.Menu(
            pystray.MenuItem("Выход", on_clicked_trei),
        ))

    return icon

def trei_start(icon):
    icon.run()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def notification_system(title, message, icon="icon.png"):
    notification = Notify()
    try:
        notification.application_name = bot.get_my_name().name
    except NameError:
        notification.application_name = "Bot"
    notification.title = title
    notification.message = message
    notification.icon = resource_path(icon)
    notification.send()


def internet_check():
    timeout = 1
    internet = False
    trying = 0
    while not internet:
        try:
            requests.head("http://www.google.com/", timeout=timeout)
            internet = True
            time.sleep(1)
        except requests.exceptions.ConnectionError:
            if trying == 1:
                notification_system('Ошибка', 'Не удалось соединиться с интернетом')
            print('Ошибка')
            trying = trying + 1
            time.sleep(5)


####################
#   ОСНОВНОЙ КОД   #
####################


""" Проверка существования токена в APPDATA и создание его при отсутствии """

icon = trei()

t2 = threading.Thread(target=trei_start, args=(icon,))
t2.start()

if debug == 1:
    notification_system('Внимание!', 'Запущена отладочная версия')

try:
    f = open(os.getenv('APPDATA') + '\\PC_Control_Bot\\token', 'r')
    f.close()
except (IOError) and (Exception):
    window = Tk()
    window.title("Тест окно")

    lbl = Label(window, text="Введите свой Токен")
    lbl.grid(column=1, row=0)

    enter_token = Entry(window)
    enter_token.grid(column=1, row=1)

    confirm_button = Button(window, text="Подтвердить", command=on_confirm)
    confirm_button.grid(column=0, row=2)

    exit_button = Button(window, text="Выйти", command=on_exit)
    exit_button.grid(column=3, row=2)

    window.mainloop()

"""Проверка и загрузка списка пользователей"""

if not os.path.exists(os.getenv('APPDATA') + '\\PC_Control_Bot\\Users.json'):
    with open(os.getenv('APPDATA') + '\\PC_Control_Bot\\Users.json', 'w') as file:
        json.dump({"verified": [], "banned": []}, file)

with open(os.getenv('APPDATA') + '\\PC_Control_Bot\\Users.json') as file:
    data = json.load(file)

verified_users = set(data['verified'])
banned_users = set(data['banned'])


token_code = open(os.getenv('APPDATA') + '\\PC_Control_Bot\\token', 'r')
token = token_code.read()
token_code.close()

alive = True

while alive == True:
    try:

        internet_check()

        bot = telebot.TeleBot(token)

        icon.icon = Image.open(resource_path("logo_work.png"))

        @bot.message_handler(commands=['start'], func=lambda message: get_user_state(message.chat.id) == None)
        def send_welcome(message):
            user_id = message.from_user.id
            if login_system(user_id) == "val":
                markup = get_keyboard()
                bot.reply_to(message, "Вывод кнопок", parse_mode='html', reply_markup=markup)
            elif login_system(user_id) == "ban":
                bot.reply_to(message,
                             "Вы заблокированы в системе. Для повторной верификации, необходимо сбросить настройки пользователей в клиенте")
            else:
                bot.reply_to(message, "Для начала работы, необходимо верифицировать аккаунт. Для этого напишите /ver")


        @bot.message_handler(commands=['ver'], func=lambda message: get_user_state(message.chat.id) == None)
        def ver_message(message):
            user_id = message.from_user.id
            if login_system(user_id) == "val":
                bot.send_message(message.chat.id, f'Не стоит {message.from_user.first_name}. Вы уже верифицированы')
            elif login_system(user_id) == "ban":
                bot.send_message(message.chat.id, f'Вы уже заблокированы')
            else:
                chat_id = message.chat.id
                user_data[chat_id] = generate_code()
                print("Используйте этот код для проверки:", user_data[chat_id])
                t1 = threading.Thread(target=code_display, args=(chat_id, message.from_user.first_name,))
                t1.start()
                bot.send_message(message.chat.id,
                                 f'Вам на экране вывелись числа для верификации, пожалуйста, введите их сюда для '
                                 f'верификации аккаунта')
                set_user_state(user_id, 'waiting_for_code')


        @bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == 'waiting_for_code')
        def check_code(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            try:
                user_code = int(message.text)
                if chat_id in user_data and user_data[chat_id] == user_code:
                    markup = get_keyboard()
                    bot.reply_to(message, "Код валиден! Вы теперь верифицированы.", parse_mode='html', reply_markup=markup)
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


        @bot.message_handler(commands=['shutdown'], func=lambda message: get_user_state(message.chat.id) == None)
        def shutdown(message):
            user_id = message.from_user.id
            if login_system(user_id) == "val":
                set_user_state(user_id, 'Selects_the_input_type_time')
                type_time = types.ReplyKeyboardMarkup(resize_keyboard=True)
                but0 = types.KeyboardButton("Часы")
                but1 = types.KeyboardButton("Минуты")
                but2 = types.KeyboardButton("Секунды")
                but3 = types.KeyboardButton("Назад")
                type_time.add(but0, but1, but2, but3)
                bot.send_message(message.chat.id, 'Как вы хотите написать время?',
                                 parse_mode='html', reply_markup=type_time)
                bot.register_next_step_handler(message, time_select1)

            elif login_system(user_id) == "ban":
                bot.reply_to(message,
                             "Вы заблокированы в системе. Для повторной верификации, необходимо сбросить настройки пользователей в клиенте")
            else:
                bot.reply_to(message, "Для начала работы, необходимо верифицировать аккаунт. Для этого напишите /ver")


        @bot.message_handler(commands=['cancel'], func=lambda message: get_user_state(message.chat.id) == None)
        def cancel(message):
            user_id = message.from_user.id
            if login_system(user_id) == "val":
                cancel = os.system('shutdown /a')
                print(cancel)
                if cancel == 1116:
                    bot.reply_to(message, 'Нет запланированного отключения')
                else:
                    bot.reply_to(message, 'Отключение отменено')
            elif login_system(user_id) == "ban":
                bot.reply_to(message,
                             "Вы заблокированы в системе. Для повторной верификации, необходимо сбросить настройки пользователей в клиенте")
            else:
                bot.reply_to(message, "Для начала работы, необходимо верифицировать аккаунт. Для этого напишите /ver")


        @bot.message_handler(commands=['ping'], func=lambda message: get_user_state(message.chat.id) == None)
        def ping(message):
            user_id = message.from_user.id
            if login_system(user_id) == "val":
                image = Image.open(resource_path("logo_ping.png"))
                icon.icon = image
                notification_system('Пинг!', 'Ваш компьютер был пинганут!', 'logo_ping.png')
                bot.reply_to(message, 'Компьютер онлайн!')
                image = Image.open(resource_path("logo_work.png"))
                icon.icon = image
            elif login_system(user_id) == "ban":
                bot.reply_to(message,
                             "Вы заблокированы в системе. Для повторной верификации, необходимо сбросить "
                             "настройки пользователей в клиенте")
            else:
                bot.reply_to(message, "Для начала работы, необходимо верифицировать аккаунт. Для этого напишите /ver")


        @bot.message_handler(commands=['screenshot'], func=lambda message: get_user_state(message.chat.id) == None)
        def screenshot(message):
            user_id = message.from_user.id
            if login_system(user_id) == "val":
                image = Image.open(resource_path("logo_screenshot.png"))
                icon.icon = image
                notification_system('Запрос на скриншот', 'Был отправлен запрос на скриншот!', 'logo_screenshot.png')
                screenshot = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
                filepath = os.getenv('APPDATA') + '\\PC_Control_Bot\\temp_screenshot.png'
                screenshot.save(filepath)
                with open(filepath, 'rb') as file:
                    bot.send_document(message.chat.id, file)
                os.remove(filepath)
                bot.send_message(message.chat.id, "Скриншот успешно отправлен!")
                image = Image.open(resource_path("logo_work.png"))
                icon.icon = image
            elif login_system(user_id) == "ban":
                bot.reply_to(message,
                             "Вы заблокированы в системе. Для повторной верификации, необходимо сбросить "
                             "настройки пользователей в клиенте")
            else:
                bot.reply_to(message, "Для начала работы, необходимо верифицировать аккаунт. Для этого напишите /ver")

        bot.polling(none_stop=True)

    except:
        image = Image.open(resource_path("logo_error.png"))
        icon.icon = image
        notification_system('Ошибка', 'Произошла ошибка, выполняется перезапуск', 'logo_error.png')
        time.sleep(5)
