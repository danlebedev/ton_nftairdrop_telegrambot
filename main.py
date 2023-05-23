import telebot
from telebot import types
import logging
import json

import config
from image_captcha import Captcha
from database import DB
from crypto import Account
from keyboard import KB

def main():
    # Включаем логирование, чтобы не пропустить важные сообщения.
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = telebot.TeleBot(config.token)
    # Загрузка всех текстов ответов бота.
    with open('texts.json') as f:
        data = json.load(f)
    # Создаем инлайл клавиатуру.
    kb = KB()
    # Объект капчи.
    cap = Captcha()
    # Словарь для хранения сообщения бота.
    bot_message = {'message': None}

    # Хэндлер на команду /start.
    @bot.message_handler(commands=['start'])
    def hand_start(message):
        kb.set_default()
        bot.send_message(
            chat_id=message.chat.id,
            text=data['hand_start'],
            reply_markup=kb.get_markup(),
        )

    # Хэндлер на удаление всех сообщений юзера.
    @bot.message_handler(func=lambda message: True)
    def delete_all_user_messages(message):
        try:
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id,
            )
        except:
            pass

    # Хэндлер для отлавливания всех callback.
    @bot.callback_query_handler(func=lambda call: True)
    def hand_call(call):
        if call.data == 'stop':
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None,
            )
            bot.clear_step_handler_by_chat_id(
                chat_id=call.message.chat.id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text=data['stop'],
            )
            bot.answer_callback_query(
                callback_query_id=call.id,
            )
        elif call.data == 'next':
            print_captcha(call)
        elif call.data == 'refresh':
            refresh_captcha(call)
        elif call.data == 'wallet':
            bot.register_next_step_handler_by_chat_id(
                chat_id=call.message.chat_id,
                callback=add_wallet,
            )

    def print_captcha(call):
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
        )
        cap.generate()
        kb.change_button_data(0, 'Обновить', 'refresh')
        # Присваивание нового объекта Message.
        bot_message['message'] = bot.send_photo(
            chat_id=call.message.chat.id,
            photo=cap.get_captcha(),
            caption=data['next'],
            reply_markup=kb.get_markup(),
        )
        bot.answer_callback_query(
            callback_query_id=call.id,
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=call.message.chat.id,
            callback=check_captcha,
        )

    def refresh_captcha(call):
        bot.clear_step_handler_by_chat_id(
            chat_id=call.message.chat.id,
        )
        cap.generate()
        # Присваивание нового объекта Message.
        bot_message['message'] = bot.edit_message_media(
            media=types.InputMediaPhoto(cap.get_captcha(), caption=data['next']),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kb.get_markup(),
        )
        bot.answer_callback_query(
            callback_query_id=call.id,
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=call.message.chat.id,
            callback=check_captcha,
        )

    def check_captcha(message):
        if cap.check(message.text):
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id,
            )
            bot.delete_message(
                chat_id=bot_message['message'].chat.id,
                message_id=bot_message['message'].message_id,
            )
            kb.delete_button(0)
            # Присваивание нового объекта Message.
            bot_message['message'] = bot.send_message(
                chat_id=message.chat.id,
                text=data['captcha_if'],
                reply_markup=kb.get_markup(),
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=add_wallet,
            )
        else:
            kb.change_button_data(0, 'Пробовать еще')
            bot.edit_message_media(
                media=types.InputMediaPhoto(
                    media=cap.get_captcha_copy(),
                    caption=data['captcha_else'],
                    has_spoiler=True,
                ),
                chat_id=bot_message['message'].chat.id,
                message_id=bot_message['message'].message_id,
                reply_markup=kb.get_markup(),
            )
            kb.change_button_data(0, 'Обновить')

    def add_wallet(message):
        acc = Account(message.text)
        db = DB(message.text)
        try:
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id,
            )
            kb.add_button(0, 'Ввести заново', 'wallet')
            if acc.check_wallet_in_blockchain():
                if not db.check_wallet_in_database():
                    db.add_wallet_in_database()
                    bot.edit_message_text(
                        text=data['add_wallet_if_if'],
                        chat_id=bot_message['message'].chat.id,
                        message_id=bot_message['message'].message_id,
                    )
                else:
                    # Присваивание нового объекта Message.
                    bot_message['message'] = bot.edit_message_text(
                        text=data['add_wallet_if_else'],
                        chat_id=bot_message['message'].chat.id,
                        message_id=bot_message['message'].message_id,
                        reply_markup=kb.get_markup(),
                    )
            else:
                # Присваивание нового объекта Message.
                bot_message['message'] = bot.edit_message_text(
                    text=acc.get_error(),
                    chat_id=bot_message['message'].chat.id,
                    message_id=bot_message['message'].message_id,
                    reply_markup=kb.get_markup(),
                )
        finally:
            db.close()


    bot.infinity_polling()


if __name__ == '__main__':
    main()