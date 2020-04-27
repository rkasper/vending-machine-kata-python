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
    __state: State              # I am a state machine! This is what state I am in.
    __display_price: int        # When we're in state State.PRICE, this is the price to display.
    __coin_return_slot: [Coin]  # The coins that the machine has ejected into the coin return slot
    __balance: int              # How much money the customers have inserted, in cents
    __products: {Product: int}  # The products that this machine sells. Maps Product to its price in cents.

    def __init__(self):
        self.__state = State.INSERT_COIN
        self.__display_price = 0
        self.__balance = 0
        self.__coin_return_slot = []
        self.__products = {Product.COLA: 100, Product.CHIPS: 50, Product.CANDY: 65}

    def make_change(self) -> [Coin]:
        coins = []
        while self.__balance > 0:
            if self.__balance >= 25:
                coins.append(Coin.QUARTER)
                self.__balance -= 25
            elif self.__balance >= 10:
                coins.append(Coin.DIME)
                self.__balance -= 10
            elif self.__balance >= 5:
                coins.append(Coin.NICKEL)
                self.__balance -= 5
        self.__balance = 0
        return coins

    def deposit_coin(self, coin: Coin) -> bool:
        if coin == Coin.PENNY:
            self.__coin_return_slot = [coin]
            return False

        if coin == Coin.NICKEL:
            self.__balance += 5
        elif coin == Coin.DIME:
            self.__balance += 10
        else:
            self.__balance += 25
        self.__coin_return_slot = []
        self.__state = State.HAS_COINS
        return True

    def display(self) -> str:
        if self.__state == State.INSERT_COIN:
            return "INSERT COIN"
        elif self.__state == State.HAS_COINS:
            return self.__display_amount(self.__balance)
        elif self.__state == State.PRICE:
            self.__state = State.INSERT_COIN
            return 'PRICE ' + self.__display_amount(self.__display_price)
        else:
            self.__state = State.INSERT_COIN
            return "THANK YOU"

    @staticmethod
    def __display_amount(amount: int) -> str:
        return '${:,.2f}'.format(amount / 100)

    def coins_returned(self) -> [Coin]:
        return self.__coin_return_slot

    def select_product(self, product: Product) -> Optional[Product]:
        price = self.__products[product]
        if self.__balance >= price:
            self.__state = State.THANK_YOU
            self.__balance -= price
            self.__coin_return_slot = self.make_change()
            return product
        else:
            self.__state = State.PRICE
            self.__display_price = price
            return None

    def return_coins(self):
        self.__coin_return_slot = self.make_change()
        self.__state = State.INSERT_COIN
