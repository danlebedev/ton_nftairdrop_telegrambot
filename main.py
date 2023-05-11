import telebot
from telebot import types
import logging

import config

def main():
    # Включаем логирование, чтобы не пропустить важные сообщения.
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = telebot.TeleBot(config.token)

    # Хэндлер на команду /start.
    @bot.message_handler(commands=['start'])
    def cmd_start(message):
        kb1 = types.KeyboardButton('Далее')
        kb2 = types.KeyboardButton('Выход')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(kb1, kb2)
        bot.send_message(
            chat_id=message.chat.id,
            text='Hello!',
            reply_markup=markup,
        )

    # Хэндлер на команду /stop и на сообщение.
    @bot.message_handler(commands=['stop'])
    @bot.message_handler(func=lambda message: message.text == 'Выход')
    def cmd_stop(message):
        bot.send_message(
            chat_id=message.chat.id,
            text='Поки-чпоки...',
            reply_markup=types.ReplyKeyboardRemove(),
        )

    bot.polling(non_stop=True, interval=0)


if __name__ == '__main__':
    main()