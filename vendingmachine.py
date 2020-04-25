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
    coin_return_slot: Coin
    balance: float

    def __init__(self):
        self.state = State.INSERT_COIN
        self.balance = 0
        self.coin_return_slot = None

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
        self.coin_return_slot = None
        self.state = State.HAS_COINS
        return True

    def display(self):
        if self.state == State.INSERT_COIN:
            return "INSERT COIN"
        elif self.state == State.HAS_COINS:
            return '${:,.2f}'.format(self.balance)
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

    def coin_returned(self):
        return self.coin_return_slot

    def select_product(self, product: Product):
        if product == Product.COLA:
            if self.balance == 1.00:
                self.state = State.THANK_YOU
                self.balance = 0
                return Product.COLA
            else:
                self.state = State.PRICE_COLA
                return None
        elif product == Product.CHIPS:
            if self.balance == 0.50:
                self.state = State.THANK_YOU
                self.balance = 0
                return Product.CHIPS
            else:
                self.state = State.PRICE_CHIPS
                return None
        else:  # product == Product.CANDY
            if self.balance == 0.65:
                self.state = State.THANK_YOU
                self.balance = 0
                return Product.CANDY
            else:
                self.state = State.PRICE_CANDY
                return None
