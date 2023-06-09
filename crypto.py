import requests

class Account:
    def __init__(self, wallet: str):
        self.wallet = wallet
        url = f'https://testnet.tonapi.io/v2/accounts/{self.wallet}'
        self.req = requests.get(url)
        self.resp_dict = self.req.json()

    def check_wallet_in_blockchain(self) -> bool:
        """Проверка на существование кошелька."""
        match self.req.status_code:
            case 200:
                return True
            case _:
                return False

    def get_balance(self) -> int:
        """Возвращает значение баланса."""
        return self.resp_dict['balance']

    def get_nano_balance(self) -> float:
        """Возвращает значение баланса с плавающей точкой."""
        return self.resp_dict['balance'] / 1_000_000_000
    
    def get_error(self) -> str:
        match self.req.status_code:
            case 400:
                return 'Вы ввели несуществующий адрес'
            case _:
                return 'Что-то пошло не так...'