from enum import Enum
from typing import Optional

from coin import Coin
from product import Product


class State(Enum):
    INSERT_COIN = 1
    HAS_COINS = 2
    THANK_YOU = 3
    PRICE = 4


class VendingMachine:
    state: State  # I am a state machine! This is what state I am in.
    display_price: int  # When we're in state State.PRICE, this is the price to display.
    coin_return_slot: [Coin]  # The coins that the machine has ejected into the coin return slot
    balance: int  # How much money the customers have inserted, in cents
    products: {Product: int}  # The products that this machine sells. The dictionary maps Product to its price in cents.

    def __init__(self):
        self.state = State.INSERT_COIN
        self.display_price = 0
        self.balance = 0
        self.coin_return_slot = []
        self.products = {Product.COLA: 100, Product.CHIPS: 50, Product.CANDY: 65}

    def make_change(self) -> [Coin]:
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

    def deposit_coin(self, coin: Coin) -> bool:
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

    def display(self) -> str:
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

    def coins_returned(self) -> [Coin]:
        return self.coin_return_slot

    def select_product(self, product: Product) -> Optional[Product]:
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

