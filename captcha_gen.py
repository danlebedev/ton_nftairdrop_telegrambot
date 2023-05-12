from captcha.image import ImageCaptcha
from random import choice


def generate_captcha():
    image = ImageCaptcha(width=300, height=100)
    symbols = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
    captcha_text = ''.join([choice(symbols) for _ in range(5)])

    # Генерация картинки капчи.
    return image.generate(captcha_text)