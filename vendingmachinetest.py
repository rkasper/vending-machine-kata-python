import unittest

from coin import Coin
from product import Product
from vendingmachine import VendingMachine


class VendingMachineTest(unittest.TestCase):
    # Make sure the unittest system works properly
    def test_unittest_works_properly(self):
        self.assertTrue(True)

    # Accept Coins
    #
    # As a vendor
    # I want a vending machine that accepts coins
    # So that I can collect money from the customer
    #
    # The vending machine will accept valid coins (nickels, dimes, and quarters) and reject invalid ones (pennies).
    # When a valid coin is inserted the amount of the coin will be added to the current amount and the display will be
    # updated. When there are no coins inserted, the machine displays INSERT COIN. Rejected coins are placed in the
    # coin return.
    #
    # NOTE: The temptation here will be to create Coin objects that know their value. However, this is not how a real
    # vending machine works. Instead, it identifies coins by their weight and size and then assigns a value to what
    # was inserted. You will need to do something similar. This can be simulated using strings, constants, enums,
    # symbols, or something of that nature.
    def test_accept_coins(self):
        vm = VendingMachine()

        # When we turn on the vending machine, it displays "INSERT COIN".
        self.assertEqual("INSERT COIN", vm.display())

        # When we add a nickel, it displays the balance: $0.05.
        self.assertTrue(vm.deposit_coin(Coin.NICKEL))
        self.assertEqual("$0.05", vm.display())
        self.assertIsNone(vm.coin_returned(), "The coin return slot should be empty.")

        # When we add another nickel, it displays the new balance: $0.10
        self.assertTrue(vm.deposit_coin(Coin.NICKEL))
        self.assertEqual("$0.10", vm.display())

        # When we add a dime, it displays the new balance: $0.20
        self.assertTrue(vm.deposit_coin(Coin.DIME))
        self.assertEqual("$0.20", vm.display())

        # When we add a quarter, it displays the new balance: $0.45
        self.assertTrue(vm.deposit_coin(Coin.QUARTER))
        self.assertEqual("$0.45", vm.display())

        # When we try to add a penny, the penny is placed in the coin return and the balance doesn't change.
        self.assertFalse(vm.deposit_coin(Coin.PENNY), "Should not accept a penny")
        self.assertEqual("$0.45", vm.display())
        self.assertEqual(Coin.PENNY, vm.coin_returned(), "Rejected penny should be in coin return slot")

    # Select Product
    #
    # As a vendor
    # I want customers to select products
    # So that I can give them an incentive to put money in the machine
    #
    # There are three products: cola for $1.00, chips for $0.50, and candy for $0.65. When the respective button is
    # pressed and enough money has been inserted, the product is dispensed and the machine displays THANK YOU. If the
    # display is checked again, it will display INSERT COIN and the current amount will be set to $0.00. If there is
    # not enough money inserted then the machine displays PRICE and the price of the item and subsequent checks of the
    # display will display either INSERT COIN or the current amount as appropriate.
    def test_select_product(self):
        vm = VendingMachine()

        # When I insert enough money and select chips,
        # then I get my cola
        #  and the display says THANK YOU
        #  and then the display says INSERT COIN
        vm.deposit_coin(Coin.QUARTER)
        vm.deposit_coin(Coin.QUARTER)
        vm.deposit_coin(Coin.QUARTER)
        vm.deposit_coin(Coin.QUARTER)
        product = vm.select_product(Product.COLA)
        self.assertEqual(Product.COLA, product)
        self.assertEqual("THANK YOU", vm.display())
        self.assertEqual("INSERT COIN", vm.display())

        # ... and then there's no money left in the machine.
        # Given there's no money in the machine
        # when  I select cola
        # then  I receive nothing
        #  and  the display tells me the price of the cola
        #  and  then the display tells me to INSERT COIN
        product = vm.select_product(Product.COLA)
        self.assertIsNone(product)
        self.assertEqual("PRICE $1.00", vm.display())
        self.assertEqual("INSERT COIN", vm.display())

        # Given there's no money in the machine
        # when  I add a coin, but it's not enough to purchase cola
        # then  I receive nothing
        #  and  the display tells me the price of the cola
        #  and  then the display tells me to INSERT COIN
        vm.deposit_coin(Coin.QUARTER)
        product = vm.select_product(Product.COLA)
        self.assertIsNone(product)
        self.assertEqual("PRICE $1.00", vm.display())
        self.assertEqual("INSERT COIN", vm.display())

        # Purchase chips for 50 cents
        product = vm.select_product(Product.CHIPS)
        self.assertIsNone(product)
        self.assertEqual("PRICE $0.50", vm.display(), "Wrong price for chips")
        self.assertEqual("INSERT COIN", vm.display())
        vm.deposit_coin(Coin.QUARTER)
        product = vm.select_product(Product.CHIPS)
        self.assertEqual(Product.CHIPS, product)
        self.assertEqual("THANK YOU", vm.display())
        self.assertEqual("INSERT COIN", vm.display())

        # Purchase candy for 65 cents
        product = vm.select_product(Product.CANDY)
        self.assertIsNone(product)
        self.assertEqual("PRICE $0.65", vm.display(), "Wrong price for candy")
        self.assertEqual("INSERT COIN", vm.display())
        vm.deposit_coin(Coin.QUARTER)
        vm.deposit_coin(Coin.QUARTER)
        vm.deposit_coin(Coin.DIME)
        vm.deposit_coin(Coin.NICKEL)
        product = vm.select_product(Product.CANDY)
        self.assertEqual(Product.CANDY, product)
        self.assertEqual("THANK YOU", vm.display())
        self.assertEqual("INSERT COIN", vm.display())


if __name__ == '__main__':
    unittest.main()
