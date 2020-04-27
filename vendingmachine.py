from enum import Enum

from coin import Coin
from product import Product


class State(Enum):
    INSERT_COIN = 1
    HAS_COINS = 2
    THANK_YOU = 3
    PRICE = 4


class VendingMachine:
    state: State
    coin_return_slot = []  # A list of Coins TODO Specify this type better
    balance: int
    products = {}  # TODO document this dictionary
    display_price: int

    def __init__(self):
        self.state = State.INSERT_COIN
        self.display_price = 0
        self.balance = 0
        self.coin_return_slot = []
        self.products = {Product.COLA : 100, Product.CHIPS : 50, Product.CANDY : 65}

    def make_change(self):
        coins = []
        while self.balance > 0:
            if self.balance >= 25:
                coins.append(Coin.QUARTER)
                self.balance -= 25
            elif self.balance >= 10:
                coins.append(Coin.DIME)
                self.balance -= 10
            elif self.balance >= 5:
                coins.append(Coin.NICKEL)
                self.balance -= 5
        self.balance = 0
        return coins

    # TODO Specify that it returns True or False
    def deposit_coin(self, coin: Coin):
        if coin == Coin.PENNY:
            self.coin_return_slot = [coin]
            return False

        if coin == Coin.NICKEL:
            self.balance += 5
        elif coin == Coin.DIME:
            self.balance += 10
        else:
            self.balance += 25
        self.coin_return_slot = []
        self.state = State.HAS_COINS
        return True

    # TODO Specify that it returns str
    def display(self):
        if self.state == State.INSERT_COIN:
            return "INSERT COIN"
        elif self.state == State.HAS_COINS:
            return '${:,.2f}'.format(self.balance / 100)
        elif self.state == State.PRICE:
            self.state = State.INSERT_COIN
            return 'PRICE ${:,.2f}'.format(self.display_price / 100)
        else:
            self.state = State.INSERT_COIN
            return "THANK YOU"

    # TODO Specify that it returns List[Coin]
    def coins_returned(self):
        return self.coin_return_slot

    # TODO Specify that it returns Product
    def select_product(self, product: Product):
        price = self.products[product]
        if self.balance >= price:
            self.state = State.THANK_YOU
            self.balance -= price
            self.coin_return_slot = self.make_change()
            return product
        else:
            self.state = State.PRICE
            self.display_price = price
            return None

