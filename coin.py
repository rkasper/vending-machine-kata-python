from enum import Enum


class Coin(Enum):
    PENNY = 0
    NICKEL = 1
    DIME = 2
    QUARTER = 3

    @staticmethod
    def value(coins: []) -> float:  # TODO How to specify that the param is [Coin]?
        val: float = 0
        for coin in coins:
            if coin == Coin.PENNY:
                val += 0.01
            elif coin == Coin.NICKEL:
                val += 0.05
            elif coin == Coin.DIME:
                val += 0.10
            elif coin == Coin.QUARTER:
                val += 0.25
        return val
