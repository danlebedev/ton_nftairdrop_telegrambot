import telebot
from telebot import types
import logging
import json

import config
from image_captcha import Captcha
from database import DB
from crypto import Account
from keyboard import KB
import telebot.storage.base_storage as strg

strg.StateStorageBase

def main():
    # Включаем логирование, чтобы не пропустить важные сообщения.
    logging.basicConfig(level=logging.DEBUG)
    # Объект бота
    bot = telebot.TeleBot(config.token)
    # Загрузка всех текстов ответов бота.
    with open('texts.json') as f:
        data = json.load(f)
    # Хранилище объекта инлайн клавиатуры.
    kb = {}
    # Хранилище объекта капчи.
    cap = {}
    # Храненилище объекта сообщения бота.
    bot_message = {}

    # Хэндлер на команду /start.
    @bot.message_handler(commands=['start'], chat_types=['private'])
    def hand_start(message):
        kb[message.chat.id] = KB()
        cap[message.chat.id] = Captcha()
        kb[message.chat.id].set_default()
        bot.send_message(
            chat_id=message.chat.id,
            text=data['hand_start'],
            reply_markup=kb[message.chat.id].get_markup(),
        )

    # Хэндлер на удаление всех сообщений юзера.
    @bot.message_handler(func=lambda message: True, chat_types=['private'])
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

    def print_captcha(call):
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
        )
        cap[call.message.chat.id].generate()
        kb[call.message.chat.id].change_button_data(0, 'Обновить', 'refresh')
        # Присваивание нового объекта Message.
        bot_message[call.message.chat.id] = bot.send_photo(
            chat_id=call.message.chat.id,
            photo=cap[call.message.chat.id].get_captcha(),
            caption=data['next'],
            reply_markup=kb[call.message.chat.id].get_markup(),
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
        cap[call.message.chat.id].generate()
        # Присваивание нового объекта Message.
        bot_message[call.message.chat.id] = bot.edit_message_media(
            media=types.InputMediaPhoto(cap[call.message.chat.id].get_captcha(), caption=data['next']),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kb[call.message.chat.id].get_markup(),
        )
        bot.answer_callback_query(
            callback_query_id=call.id,
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=call.message.chat.id,
            callback=check_captcha,
        )

    def check_captcha(message):
        delete_all_user_messages(message)
        if cap[message.chat.id].check(message.text):
            kb[message.chat.id].delete_button(0)
            pass_captcha(message, data['captcha_if'])
        else:
            kb[message.chat.id].change_button_data(0, 'Пробовать еще')
            bot.edit_message_media(
                media=types.InputMediaPhoto(
                    media=cap[message.chat.id].get_captcha_copy(),
                    caption=data['captcha_else'],
                    has_spoiler=True,
                ),
                chat_id=bot_message[message.chat.id].chat.id,
                message_id=bot_message[message.chat.id].message_id,
                reply_markup=kb[message.chat.id].get_markup(),
            )
            kb[message.chat.id].change_button_data(0, 'Обновить')

    def pass_captcha(message, text):
        if bot_message[message.chat.id].content_type != 'text':
            bot.delete_message(
                    chat_id=bot_message[message.chat.id].chat.id,
                    message_id=bot_message[message.chat.id].message_id,
                )
            # Присваивание нового объекта Message.
            bot_message[message.chat.id] = bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=kb[message.chat.id].get_markup(),
            )
        else:
            try:
                bot.edit_message_text(
                    text=text,
                    chat_id=bot_message[message.chat.id].chat.id,
                    message_id=bot_message[message.chat.id].message_id,
                    reply_markup=kb[message.chat.id].get_markup(),
                )
            except:
                pass
        bot.register_next_step_handler_by_chat_id(
            chat_id=message.chat.id,
            callback=add_wallet,
        )

    def add_wallet(message):
        acc = Account(message.text)
        db = DB(message.text, message.from_user.id)
        try:
            delete_all_user_messages(message)
            if acc.check_wallet_in_blockchain():
                if not db.check_wallet_in_database():
                    db.add_wallet_in_database()
                    bot.edit_message_text(
                        text=data['add_wallet_if_if'],
                        chat_id=bot_message[message.chat.id].chat.id,
                        message_id=bot_message[message.chat.id].message_id,
                    )
                else:
                    pass_captcha(message, f"{data['add_wallet_if_else']}\n{data['re_wallet']}",)
            else:
                pass_captcha(message, f"{acc.get_error()}\n{data['re_wallet']}",)
        finally:
            db.close()


    bot.infinity_polling()


if __name__ == '__main__':
    main()