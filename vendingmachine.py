from enum import Enum

from coin import Coin
from product import Product


class State(Enum):
    INSERT_COIN = 1
    HAS_COINS = 2
    THANK_YOU = 3
    PRICE_COLA = 4
    PRICE_CHIPS = 5
    PRICE_CANDY = 6


class VendingMachine:
    state: State
    coin_return_slot = []  # A list of Coins TODO Specify this type better
    balance: float  # TODO make this an int or find a currency class. float sucks - currency precision gets lost!

    def __init__(self):
        self.state = State.INSERT_COIN
        self.balance = 0
        self.coin_return_slot = []

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
        elif self.state == State.PRICE_COLA:
            self.state = State.INSERT_COIN
            return "PRICE $1.00"
        elif self.state == State.PRICE_CHIPS:
            self.state = State.INSERT_COIN
            return "PRICE $0.50"
        elif self.state == State.PRICE_CANDY:
            self.state = State.INSERT_COIN
            return "PRICE $0.65"
        else:
            self.state = State.INSERT_COIN
            return "THANK YOU"

    # TODO Specify that it returns List[Coin]
    def coins_returned(self):
        return self.coin_return_slot

    # TODO Specify that it returns Product
    def select_product(self, product: Product):
        if product == Product.COLA:
            if self.balance >= 100:
                self.state = State.THANK_YOU
                self.balance -= 100
                self.coin_return_slot = self.make_change()
                return Product.COLA
            else:
                self.state = State.PRICE_COLA
                return None
        elif product == Product.CHIPS:
            if self.balance >= 50:
                self.state = State.THANK_YOU
                self.balance -= 50
                self.coin_return_slot = self.make_change()
                return Product.CHIPS
            else:
                self.state = State.PRICE_CHIPS
                return None
        else:  # product == Product.CANDY
            if self.balance >= 65:
                self.state = State.THANK_YOU
                self.balance -= 65
                self.coin_return_slot = self.make_change()
                return Product.CANDY
            else:
                self.state = State.PRICE_CANDY
                return None
