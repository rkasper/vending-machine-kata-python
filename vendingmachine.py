from enum import Enum
from typing import Optional

from coin import Coin
from product import Product


class State(Enum):
    INSERT_COIN = 1
    HAS_COINS = 2
    THANK_YOU = 3
    PRICE = 4
    SOLD_OUT = 5
    EXACT_CHANGE_ONLY = 6


class VendingMachine:
    __inventory: {Product: int}  # A list of Products and the number of each one that we have in inventory
    __state: State               # I am a state machine! This is what state I am in.
    __display_price: int         # When we're in state State.PRICE, this is the price to display.
    __coin_return_slot: [Coin]   # The coins that the machine has ejected into the coin return slot
    __balance: int               # How much money the customers have inserted, in cents
    __price_list: {Product: int}   # The products that this machine sells. Maps Product to its price in cents.
    __customers_coins: {Coin: int}  # The number of each kind of coin that the customer has inserted for a new purchase

    def __init__(self, inventory: {Product: int} = {Product.CANDY: 42, Product.COLA: 42, Product.CHIPS: 42}):
        self.__inventory = inventory
        self.__state = State.INSERT_COIN
        self.__display_price = 0
        self.__balance = 0
        self.__coin_return_slot = []
        self.__price_list = {Product.COLA: 100, Product.CHIPS: 50, Product.CANDY: 65}
        self.__customers_coins = {Coin.QUARTER: 0, Coin.DIME: 0, Coin.NICKEL: 0}

    # TODO move this method lower down in the class
    def __can_make_change(self, change_needed: int) -> [Coin]:
        coins_to_return = []
        while change_needed > 0:
            if change_needed >= 25:
                if self.__customers_coins[Coin.QUARTER] > 0:
                    self.__customers_coins[Coin.QUARTER] -= 1;
                    coins_to_return.append(Coin.QUARTER)
                    change_needed -= 25
                elif self.__customers_coins[Coin.DIME] > 0:
                    self.__customers_coins[Coin.DIME] -= 1
                    coins_to_return.append(Coin.DIME)
                    change_needed -= 10
                elif self.__customers_coins[Coin.NICKEL] > 0:
                    self.__customers_coins[Coin.NICKEL] -= 1
                    coins_to_return.append(Coin.NICKEL)
                    change_needed -= 5
                else:
                    return []
            elif change_needed >= 10:
                if self.__customers_coins[Coin.DIME] > 0:
                    self.__customers_coins[Coin.DIME] -= 1
                    coins_to_return.append(Coin.DIME)
                    change_needed -= 10
                elif self.__customers_coins[Coin.NICKEL] > 0:
                    self.__customers_coins[Coin.NICKEL] -= 1
                    coins_to_return.append(Coin.NICKEL)
                    change_needed -= 5
                else:
                    return []
            elif change_needed >= 5:
                if self.__customers_coins[Coin.NICKEL] > 0:
                    self.__customers_coins[Coin.NICKEL] -= 1
                    coins_to_return.append(Coin.NICKEL)
                    change_needed -= 5
                else:
                    return []
        return coins_to_return

    # TODO rename to __return_customers_coins()
    # TODO move this method lower down in the class
    def __make_change(self) -> [Coin]:
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

        self.__customers_coins[coin] += 1
        if coin == Coin.NICKEL:
            self.__balance += 5
        elif coin == Coin.DIME:
            self.__balance += 10
        else:
            self.__balance += 25
        self.__coin_return_slot = []
        self.__state = State.HAS_COINS
        return True

    def view_display_message(self) -> str:
        if self.__state == State.INSERT_COIN:
            return "INSERT COIN"
        elif self.__state == State.HAS_COINS:
            return self.__display_amount(self.__balance)
        elif self.__state == State.PRICE:
            self.__state = State.INSERT_COIN
            return 'PRICE ' + self.__display_amount(self.__display_price)
        elif self.__state == State.THANK_YOU:
            self.__state = State.INSERT_COIN
            return "THANK YOU"
        elif self.__state == State.SOLD_OUT:
            if self.__balance == 0:
                self.__state = State.INSERT_COIN
            else:
                self.__state = State.HAS_COINS
            return "SOLD OUT"
        else:  # state is EXACT_CHANGE_ONLY
            return "EXACT CHANGE ONLY"

    @staticmethod
    def __display_amount(amount: int) -> str:
        return '${:,.2f}'.format(amount / 100)

    def check_coin_return_slot(self) -> [Coin]:
        return self.__coin_return_slot

    def select_product(self, product: Product) -> Optional[Product]:
        price = self.__price_list[product]
        if self.__is_in_inventory(product):
            if self.__balance >= price:
                change_needed = self.__balance - price
                change = self.__can_make_change(change_needed)  # TODO don't compute change if we don't need it
                if change_needed == 0 or change:
                    self.__remove_from_inventory(product)
                    self.__state = State.THANK_YOU
                    self.__balance = 0  # because I'm delivering both the product and the change
                    self.__coin_return_slot = change
                    return product
                else:  # can't make change
                    self.__state = State.EXACT_CHANGE_ONLY
                    return None
            else:  # customer didn't insert enough money
                self.__state = State.PRICE
                self.__display_price = price
                return None
        else:  # selected product is not in inventory
            self.__state = State.SOLD_OUT
            return None

    def __is_in_inventory(self, product: Product) -> bool:
        quantity = self.__inventory[product]
        return quantity > 0

    def __remove_from_inventory(self, product: Product):
        self.__inventory[product] -= 1

    # TODO Return the same coins that the customer inserted: __customers_coins. Change __make_change() so it returns
    # __customers_coins, and then reset __customers_coins so there are 0 coins.
    def press_coin_return_button(self):
        self.__coin_return_slot = self.__make_change()
        self.__state = State.INSERT_COIN
