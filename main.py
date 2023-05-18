import telebot
from telebot import types
import logging

import config
from captcha_gen import generate_captcha, check_captcha
from database import check_wallet_in_database, add_wallet_in_database

def main():
    # Включаем логирование, чтобы не пропустить важные сообщения.
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = telebot.TeleBot(config.token)

    # Хэндлер на команду /start.
    @bot.message_handler(commands=['start'])
    def hand_start(message):
        kb1 = types.KeyboardButton('Далее')
        kb2 = types.KeyboardButton('Выход')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(kb1, kb2)
        bot.send_message(
            chat_id=message.chat.id,
            text='Hello!',
            reply_markup=markup,
        )

    # Хэндлер на команду /stop и на сообщение "Выход".
    @bot.message_handler(commands=['stop'])
    @bot.message_handler(func=lambda message: message.text == 'Выход')
    def hand_stop(message):
        bot.send_message(
            chat_id=message.chat.id,
            text='Поки-чпоки...',
            reply_markup=types.ReplyKeyboardRemove(),
        )

    # Хэндлер на сообщение "Далее".
    @bot.message_handler(func=lambda message: message.text == 'Далее')
    def hand_next(message):
        bot.send_photo(
            chat_id=message.chat.id,
            photo=(generate_captcha()),
            caption='CAPTCHA',
            reply_markup=types.ReplyKeyboardRemove(),
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=message.chat.id,
            callback=captcha,
        )

    def captcha(message):
        if check_captcha(message.text):
            bot.send_message(
                chat_id=message.chat.id,
                text='Введите свой TonCoin кошелек...',
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=add_wallet,
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='Вали отсюда стиралка',
            )

    def add_wallet(message):
        if not check_wallet_in_database(message.text):
            add_wallet_in_database(message.text)
            bot.send_message(
                chat_id=message.chat.id,
                text='Вы были добавлены в качесте участника',
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='Данный кошелек уже зарегистрирован'
            )


    bot.infinity_polling()


if __name__ == '__main__':
    main()