from enum import Enum

from coin import Coin
from product import Product


class State(Enum):
    INSERT_COIN = 1
    HAS_COINS = 2
    THANK_YOU = 3


class VendingMachine:
    state: State
    coin_return_slot: Coin
    balance: float

    def __init__(self):
        self.state = State.INSERT_COIN
        self.balance = 0
        self.coin_return_slot = Coin.NONE

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
        self.state = State.HAS_COINS
        return True

    def display(self):
        if self.state == State.INSERT_COIN:
            return "INSERT COIN"
        elif self.state == State.HAS_COINS:
            return '${:,.2f}'.format(self.balance)
        else:
            self.state = State.INSERT_COIN
            return "THANK YOU"

    def coin_returned(self):
        return self.coin_return_slot

    def select_product(self, product: Product):
        if self.balance == 1:
            self.state = State.THANK_YOU
            self.balance = 0
            return Product.CHIPS
        else:
            return None
