import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback


bot = telebot.TeleBot(TOKEN)

# Проверка работоспособности приветствия
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = f"Приветствую {message.chat.username}!\nЧтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>"
    bot.reply_to(message, text)


# Отображение доступных валют для конвертации
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


# Реализаца функционала конвертации ботом. Сама конвертация представлена в классе Convertor
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')  # Предполагается три значения "из какой валюты", "в какую валюту", "кол-во"

        answer = Convertor.get_price(*values)  # Сам процесс конвертации
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()
