import requests

class Account:
    def __init__(self, wallet: str):
        self.wallet = wallet
        url = f'https://testnet.tonapi.io/v2/accounts/{self.wallet}'
        self.req = requests.get(url)
        self.resp_dict = self.req.json()

    def check_wallet(self):
        """Проверка на существование кошелька."""
        match self.req.status_code:
            case 200:
                return self.get_nano_balance()
            case 400:
                return self.get_error()
            case _:
                return None

    def get_balance(self):
        """Возвращает значение баланса."""
        return self.resp_dict['balance']

    def get_nano_balance(self):
        """Возвращает значение баланса с плавающей точкой."""
        return self.resp_dict['balance'] / 1_000_000_000
    
    def get_error(self):
        return 'Вы ввели не существующий адрес'
        