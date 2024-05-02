import telebot
import random
import json
import os

TOKEN = '5169915860:AAFbTMdwuktxXRvpTzZdLqDOVHtrjUP8X5Y'  # Токен, полученный от BotFather
bot = telebot.TeleBot(TOKEN)

VALID_CODE = random.randint(100000, 999999)  # Сгенерированный код, который выводится в консоль при запуске скрипта
print("Используйте этот код для проверки:", VALID_CODE)

filename = 'Users.json'

# Проверка наличия файла и загрузка данных
if not os.path.exists(filename):
    with open(filename, 'w') as file:
        json.dump({"verified": [], "banned": []}, file)

with open(filename) as file:
    data = json.load(file)

verified_users = set(data['verified'])
banned_users = set(data['banned'])

def save_data():
    with open(filename, 'w') as file:
        json.dump({"verified": list(verified_users), "banned": list(banned_users)}, file)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in banned_users:
        bot.reply_to(message, "Вы заблокированы и не можете проверять коды.")
    elif user_id in verified_users:
        bot.reply_to(message, "Вы уже верифицированы.")
    else:
        bot.reply_to(message, "Привет! Отправь мне код для проверки. У вас есть 3 попытки.")

@bot.message_handler(func=lambda message: True)
def check_code(message):
    user_id = message.from_user.id
    if user_id in banned_users:
        bot.reply_to(message, "Вы заблокированы и не можете проверять коды.")
    elif user_id in verified_users:
        bot.reply_to(message, "Вы уже верифицированы. ")
    else:
        try:
            user_code = int(message.text)
            if user_code == VALID_CODE:
                verified_users.add(user_id)
                save_data()
                bot.reply_to(message, "Код валиден! Вы теперь верифицированы.")
            else:
                bot.reply_to(message, "Код не валиден. Вы заблокированы.")
                banned_users.add(user_id)
                save_data()
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите 6-значный числовой код.")

bot.polling()
