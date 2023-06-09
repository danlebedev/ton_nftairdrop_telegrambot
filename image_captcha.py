from captcha.image import ImageCaptcha
from random import choice
from copy import copy


class Captcha:
    def __init__(self):
        self.image = ImageCaptcha(width=250, height=100, font_sizes=(60, 64, 68))
        self.symbols = [
            '0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9',
        ]
    
    def generate(self):
        self.text = ''.join([choice(self.symbols) for _ in range(6)])
        self.captcha = self.image.generate(self.text)
        self.captcha_copy = copy(self.captcha)

    def get_text(self):
        return self.text
    
    def get_captcha(self):
        return self.captcha
    
    def get_captcha_copy(self):
        return self.captcha_copy
    
    def check(self, message):
        if message == self.text:
            return True
        else:
            return False
        