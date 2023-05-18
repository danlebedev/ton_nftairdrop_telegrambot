from captcha.image import ImageCaptcha
from random import choice

# Словарь для хранения текста капчи.
captcha_text = {'text': ''}
def generate_captcha():
    image = ImageCaptcha(width=300, height=100)
    symbols = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
    captcha_text['text'] = ''.join([choice(symbols) for _ in range(6)])

    # Генерация картинки капчи.
    return image.generate(captcha_text['text'])

def check_captcha(message: str) -> bool:
    if message == captcha_text['text']:
        return True
    else:
        return False