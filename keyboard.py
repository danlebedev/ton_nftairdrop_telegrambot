from telebot import types

class KB:
    def __init__(self):
        self.set_default()

    def create_buttons(self):
        self.markup = types.InlineKeyboardMarkup(
            keyboard = [
                [types.InlineKeyboardButton(
                    text=kb['text'],
                    callback_data=kb['call'],
                ) for kb in self.kb_data]
            ],
        )

    def change_button_data(self, button: int, text: str=None, call: str=None):
        """
        button - позиция кнопки (первая - 0).
        text - текст кнопки, если не указан то не меняется.
        call - callback кнопки, если не указан то не меняется.
        """
        if text:
            self.kb_data[button]['text'] = text
        if call:
            self.kb_data[button]['call'] = call
        self.create_buttons()

    def delete_button(self, button: int):
        """
        button - позиция кнопки (первая - 0).
        """
        del self.kb_data[button]
        self.create_buttons()
        
    def add_button(self, button: int, text: str, call: str):
        data = {'text': text, 'call': call}
        self.kb_data.insert(button, data)
        self.create_buttons()

    def get_markup(self):
        return self.markup

    def set_default(self):
        self.kb_data = [
            {
                'text': 'Далее',
                'call': 'next',
            },
            {
                'text': 'Выход',
                'call': 'stop',
            },
        ]
        self.create_buttons()

kb = KB()
print(kb.get_markup())