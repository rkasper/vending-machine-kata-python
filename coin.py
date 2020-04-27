from enum import Enum


class Coin(Enum):
    PENNY = 0
    NICKEL = 1
    DIME = 2
    QUARTER = 3

    @staticmethod
    def value(coins) -> float:
        sum: float = 0;
        for coin in coins:
            if coin == Coin.PENNY:
                sum += 0.01
            elif coin == Coin.NICKEL:
                sum += 0.05
            elif coin == Coin.DIME:
                sum += 0.10
            elif coin == Coin.QUARTER:
                sum += 0.25
        return sum
