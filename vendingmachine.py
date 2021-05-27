from abc import abstractmethod
from enum import Enum
from typing import Optional

from coin import Coin
from product import Product


class State(Enum):
    INSERT_COIN = 1
    HAS_CUSTOMER_COINS = 2
    THANK_YOU = 3
    PRICE = 4
    SOLD_OUT = 5
    EXACT_CHANGE_ONLY = 6


class VendingMachineState:
    @staticmethod
    def _display_amount(amount: int) -> str:
        return '${:,.2f}'.format(amount / 100)

    @abstractmethod
    def view_display_message(self, vm):
        pass


class InsertCoinState(VendingMachineState):
    def view_display_message(self, vm):
        return "INSERT COIN"


class HasCustomerCoinsState(VendingMachineState):
    def view_display_message(self, vm):
        return VendingMachineState._display_amount(vm.get_balance())


class ThankYouState(VendingMachineState):
    def view_display_message(self, vm):
        vm.set_vm_state_to_insert_coin_state()
        return "THANK YOU"


class PriceState(VendingMachineState):
    def view_display_message(self, vm):
        vm.set_vm_state_to_insert_coin_state()
        return 'PRICE ' + VendingMachineState._display_amount(vm.get_display_price())


class SoldOutState(VendingMachineState):
    def view_display_message(self, vm):
        if vm.get_balance() == 0:
            vm.set_state_to_insert_coin()
            vm.set_vm_state_to_insert_coin_state()
        else:
            vm.set_state_to_has_customer_coins()
            vm.set_vm_state_to_has_customer_coins_state()
        return "SOLD OUT"


class VendingMachine:
    __inventory: {Product: int}  # A list of Products and the number of each one that we have in inventory

    # TODO Refactor from state logic to the State design pattern. Use VendingMachineState instead of State.
    __state: State               # I am a state machine! This is what state I am in.
    __vm_state: VendingMachineState  # I am a state machine following the State design pattern!

    __display_price: int         # When we're in state State.PRICE, this is the price to display.
    __coin_return_slot: [Coin]   # The coins that the machine has ejected into the coin return slot
    __balance: int               # How much money the customers have inserted, in cents
    __price_list: {Product: int}   # The products that this machine sells. Maps Product to its price in cents.
    __customers_coins: {Coin: int}  # The number of each kind of coin that the customer has inserted for a new purchase
    __coin_vault: {Coin: int}    # The coins I've collected from customer purchases

    def __init__(self, inventory=None):
        if inventory is None:
            inventory = {Product.CANDY: 42, Product.COLA: 42, Product.CHIPS: 42}
        self.__inventory = inventory

        self.__state = State.INSERT_COIN
        self.__vm_state = InsertCoinState()

        self.__display_price = 0
        self.__balance = 0
        self.__coin_return_slot = []
        self.__price_list = {Product.COLA: 100, Product.CHIPS: 50, Product.CANDY: 65}
        self.__customers_coins = self.__initialize_with_no_coins()
        self.__coin_vault = self.__initialize_with_no_coins()

    # TODO Refactor these into a single "transition to state" method.
    def set_state_to_insert_coin(self):
        self.__state = State.INSERT_COIN

    def set_vm_state_to_insert_coin_state(self):
        self.__vm_state = InsertCoinState()

    def set_state_to_has_customer_coins(self):
        self.__state = State.HAS_CUSTOMER_COINS

    def set_vm_state_to_has_customer_coins_state(self):
        self.__vm_state = HasCustomerCoinsState()

    def get_balance(self):
        return self.__balance

    def get_display_price(self):
        return self.__display_price

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

        self.__state = State.HAS_CUSTOMER_COINS
        self.__vm_state = HasCustomerCoinsState()

        return True

    def view_display_message(self) -> str:
        if self.__state == State.INSERT_COIN:
            # return "INSERT COIN"
            return self.__vm_state.view_display_message(self)
            # return InsertCoinState().view_display_message(self)
        elif self.__state == State.HAS_CUSTOMER_COINS:
            # return self.__display_amount(self.__balance)
            return self.__vm_state.view_display_message(self)
        elif self.__state == State.PRICE:
            self.__state = State.INSERT_COIN
            # self.__vm_state = InsertCoinState()
            # return 'PRICE ' + self.__display_amount(self.__display_price)
            return self.__vm_state.view_display_message(self)
        elif self.__state == State.THANK_YOU:
            self.__state = State.INSERT_COIN
            # return "THANK YOU"
            return self.__vm_state.view_display_message(self)
        elif self.__state == State.SOLD_OUT:
            # if self.__balance == 0:
            #     self.__state = State.INSERT_COIN
            #     self.__vm_state = InsertCoinState()
            # else:
            #     self.__state = State.HAS_CUSTOMER_COINS
            #     self.__vm_state = HasCustomerCoinsState()
            # return "SOLD OUT"
            return self.__vm_state.view_display_message(self)
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
                change_to_make = self.__balance - price
                change = self.__make_change(change_to_make)
                # Try to make change from the customer's coins
                # if not change:
                #     # Try to make change from the machine's coin vault
                #     change = self.__make_change_from_coin_vault(change_to_make)
                if change_to_make == 0 or change:  # customer can make the purchase
                    self.__remove_from_inventory(product)
                    if change_to_make == 0:  # Take all the customer's coins
                        self.__move_all_of_customers_coins_to_vault()
                    # else when we made change, it got taken care of

                    self.__state = State.THANK_YOU
                    self.__vm_state = ThankYouState()

                    self.__balance = 0  # because I'm delivering both the product and the change
                    self.__coin_return_slot = change
                    return product
                else:  # can't make change
                    self.__state = State.EXACT_CHANGE_ONLY
                    return None
            else:  # customer didn't insert enough money
                self.__state = State.PRICE
                self.__vm_state = PriceState()

                self.__display_price = price
                return None
        else:  # selected product is not in inventory
            self.__state = State.SOLD_OUT
            self.__vm_state = SoldOutState()
            return None

    def __move_all_of_customers_coins_to_vault(self):
        self.__coin_vault[Coin.QUARTER] += self.__customers_coins[Coin.QUARTER]
        self.__coin_vault[Coin.DIME] += self.__customers_coins[Coin.DIME]
        self.__coin_vault[Coin.NICKEL] += self.__customers_coins[Coin.NICKEL]
        self.__customers_coins = self.__initialize_with_no_coins()

    @staticmethod
    def __initialize_with_no_coins():
        return {Coin.QUARTER: 0, Coin.DIME: 0, Coin.NICKEL: 0}

    def __is_in_inventory(self, product: Product) -> bool:
        quantity = self.__inventory[product]
        return quantity > 0

    def __remove_from_inventory(self, product: Product):
        self.__inventory[product] -= 1

    # TODO There's a lot of untested code here! Add all the tests.
    # TODO Method too long - refactor it
    def __make_change(self, change_to_make: int) -> [Coin]:
        coins_to_return = []
        while change_to_make > 0:
            if change_to_make >= 25:
                if self.__remove_customer_coin_from_cache_if_possible(Coin.QUARTER):
                    coins_to_return.append(Coin.QUARTER)
                    change_to_make -= 25
                elif self.__remove_customer_coin_from_cache_if_possible(Coin.DIME):
                    coins_to_return.append(Coin.DIME)
                    change_to_make -= 10
                elif self.__remove_customer_coin_from_cache_if_possible(Coin.NICKEL):
                    coins_to_return.append(Coin.NICKEL)
                    change_to_make -= 5
                elif self.__remove_coin_from_coin_vault_if_possible(Coin.QUARTER):
                    coins_to_return.append(Coin.QUARTER)
                    change_to_make -= 25
                elif self.__remove_coin_from_coin_vault_if_possible(Coin.DIME):
                    coins_to_return.append(Coin.DIME)
                    change_to_make -= 10
                elif self.__remove_coin_from_coin_vault_if_possible(Coin.NICKEL):
                    coins_to_return.append(Coin.NICKEL)
                    change_to_make -= 5
                else:
                    return []  # Can't make change
            elif change_to_make >= 10:
                if self.__remove_customer_coin_from_cache_if_possible(Coin.DIME):
                    coins_to_return.append(Coin.DIME)
                    change_to_make -= 10
                elif self.__remove_customer_coin_from_cache_if_possible(Coin.NICKEL):
                    coins_to_return.append(Coin.NICKEL)
                    change_to_make -= 5
                elif self.__remove_coin_from_coin_vault_if_possible(Coin.DIME):
                    coins_to_return.append(Coin.DIME)
                    change_to_make -= 10
                elif self.__remove_coin_from_coin_vault_if_possible(Coin.NICKEL):
                    coins_to_return.append(Coin.NICKEL)
                    change_to_make -= 5
                else:
                    return []  # Can't make change
            elif change_to_make >= 5:
                if self.__remove_customer_coin_from_cache_if_possible(Coin.NICKEL):
                    coins_to_return.append(Coin.NICKEL)
                    change_to_make -= 5
                elif self.__remove_coin_from_coin_vault_if_possible(Coin.NICKEL):
                    coins_to_return.append(Coin.NICKEL)
                    change_to_make -= 5
                else:
                    return []  # Can't make change
        return coins_to_return

    def __remove_customer_coin_from_cache_if_possible(self, coin: Coin) -> bool:
        if self.__is_customer_coin_still_available(coin):
            self.__remove_customers_coin_from_cache(coin)
            return True
        else:
            return False

    def __remove_coin_from_coin_vault_if_possible(self, coin: Coin) -> bool:
        if self.__is_coin_in_vault(coin):
            self.__remove_coin_from_vault(coin)
            return True
        else:
            return False

    def __remove_customers_coin_from_cache(self, coin: Coin):
        self.__customers_coins[coin] -= 1

    def __remove_coin_from_vault(self, coin: Coin):
        self.__coin_vault[coin] -= 1

    def __is_customer_coin_still_available(self, coin: Coin) -> bool:
        return self.__customers_coins[coin] > 0

    def __is_coin_in_vault(self, coin: Coin) -> bool:
        return self.__coin_vault[coin] > 0

    def press_coin_return_button(self):
        self.__balance = 0

        self.__state = State.INSERT_COIN
        self.__vm_state = InsertCoinState()

        self.__coin_return_slot = []
        for i in range(0, self.__customers_coins[Coin.QUARTER]):
            self.__coin_return_slot.append(Coin.QUARTER)
        for i in range(0, self.__customers_coins[Coin.DIME]):
            self.__coin_return_slot.append(Coin.DIME)
        for i in range(0, self.__customers_coins[Coin.NICKEL]):
            self.__coin_return_slot.append(Coin.NICKEL)
