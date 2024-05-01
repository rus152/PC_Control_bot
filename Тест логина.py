import telebot
import random

# Токен, полученный от BotFather
TOKEN = '5169915860:AAFbTMdwuktxXRvpTzZdLqDOVHtrjUP8X5Y'
bot = telebot.TeleBot(TOKEN)

VALID_CODE = random.randint(100000, 999999)  # Сгенерированный код, который выводится в консоль при запуске скрипта
print("Используйте этот код для проверки:", VALID_CODE)

# Словари для хранения состояний и количества попыток пользователей
user_states = {}
user_attempts = {}
banned_users = set()

def get_user_state(user_id):
    return user_states.get(user_id, None)

def set_user_state(user_id, state):
    user_states[user_id] = state

def decrease_attempt(user_id):
    if user_id in user_attempts:
        user_attempts[user_id] -= 1
    else:
        user_attempts[user_id] = 2  # Первая попытка использована, остается еще две

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in banned_users:
        bot.reply_to(message, "Вы заблокированы и не можете проверять коды.")
    else:
        set_user_state(user_id, 'waiting_for_code')  # Устанавливаем состояние ожидания кода
        bot.reply_to(message, "Привет! Отправь мне код для проверки. У вас есть 3 попытки.")

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == 'waiting_for_code')
def check_code(message):
    user_id = message.from_user.id
    if user_id in banned_users:
        bot.reply_to(message, "Вы заблокированы и не можете проверять коды.")
        return

    try:
        user_code = int(message.text)
        if user_code == VALID_CODE:
            bot.reply_to(message, "Код валиден!")
            set_user_state(user_id, None)  # Сбрасываем состояние после проверки
        else:
            decrease_attempt(user_id)
            if user_attempts[user_id] > 0:
                bot.reply_to(message, f"Код не валиден. У вас осталось {user_attempts[user_id]} попыток.")
            else:
                banned_users.add(user_id)
                bot.reply_to(message, "Вы использовали все попытки и теперь заблокированы.")
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите 6-значный числовой код.")

@bot.message_handler(func=lambda message: True)  # Обработчик для всех других сообщений
def handle_other_messages(message):
    user_id = message.from_user.id
    if get_user_state(user_id) is None:
        if user_id in banned_users:
            bot.reply_to(message, "Вы заблокированы и не можете проверять коды.")
        else:
            bot.reply_to(message, "Напиши /start, чтобы начать проверку кода.")

bot.polling()