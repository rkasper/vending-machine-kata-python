from coin import Coin


class VendingMachine:
    coin_return_slot: Coin
    balance: float

    def __init__(self):
        self.balance = 0
        self.coin_return_slot = Coin.NONE

    def accept_coin(self, coin: Coin):
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
        return True

    def display(self):
        if self.balance == 0:
            return "INSERT COIN"
        else:
            return '${:,.2f}'.format(self.balance)

    def coin_returned(self):
        return self.coin_return_slot
