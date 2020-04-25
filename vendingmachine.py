from coin import Coin
from product import Product


class VendingMachine:
    coin_return_slot: Coin
    balance: float
    next_display_message: str

    def __init__(self):
        self.balance = 0
        self.coin_return_slot = Coin.NONE
        self.next_display_message = "INSERT COIN"

    def deposit_coin(self, coin: Coin):
        if coin == Coin.PENNY:
            self.coin_return_slot = Coin.PENNY
            return False

        if coin == Coin.NICKEL:
            self.balance += 0.05
        elif coin == Coin.DIME:
            self.balance += 0.10
        else:
            self.balance += 0.25
        self.coin_return_slot = Coin.NONE
        self.next_display_message = '${:,.2f}'.format(self.balance)
        return True

    def display(self):
        return self.next_display_message

    def coin_returned(self):
        return self.coin_return_slot

    def select_product(self, product: Product):
        self.next_display_message = "THANK YOU"
        return Product.CHIPS
