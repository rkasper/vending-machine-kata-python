import unittest

from coin import Coin


class CoinTest(unittest.TestCase):
    def test_value(self):
        self.assertEqual(0, Coin.value([]))
        self.assertEqual(1, Coin.value([Coin.PENNY]))
        self.assertEqual(100, Coin.value([Coin.NICKEL, Coin.DIME, Coin.DIME, Coin.QUARTER, Coin.QUARTER, Coin.QUARTER]))
