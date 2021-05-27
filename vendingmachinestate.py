from abc import abstractmethod


class VendingMachineState:
    # Singleton pattern implementation borrowed from
    # https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
    _instance = None

    @staticmethod
    def instance():
        pass

    @staticmethod
    def transition_to(vm, next_vm_state):
        vm.set_vm_state(next_vm_state)

    @staticmethod
    def _display_amount(amount: int) -> str:
        return '${:,.2f}'.format(amount / 100)

    @abstractmethod
    def view_display_message(self, vm) -> str:
        return ""


class InsertCoinState(VendingMachineState):
    @staticmethod
    def instance():
        if InsertCoinState._instance == None:
            InsertCoinState()
        return InsertCoinState._instance

    def __init__(self):
        """ Virtually private constructor. """
        if InsertCoinState._instance != None:
            raise Exception("This class is a singleton!")
        else:
            InsertCoinState._instance = self

    def view_display_message(self, vm):
        return "INSERT COIN"


class HasCustomerCoinsState(VendingMachineState):
    @staticmethod
    def instance():
        if HasCustomerCoinsState._instance == None:
            HasCustomerCoinsState()
        return HasCustomerCoinsState._instance

    def __init__(self):
        """ Virtually private constructor. """
        if HasCustomerCoinsState._instance != None:
            raise Exception("This class is a singleton!")
        else:
            HasCustomerCoinsState._instance = self

    def view_display_message(self, vm):
        return VendingMachineState._display_amount(vm.get_balance())


class ThankYouState(VendingMachineState):
    @staticmethod
    def instance():
        if ThankYouState._instance == None:
            ThankYouState()
        return ThankYouState._instance

    def __init__(self):
        """ Virtually private constructor. """
        if ThankYouState._instance != None:
            raise Exception("This class is a singleton!")
        else:
            ThankYouState._instance = self

    def view_display_message(self, vm):
        self.transition_to(vm, InsertCoinState.instance())
        return "THANK YOU"


class PriceState(VendingMachineState):
    @staticmethod
    def instance():
        if PriceState._instance == None:
            PriceState()
        return PriceState._instance

    def __init__(self):
        """ Virtually private constructor. """
        if PriceState._instance != None:
            raise Exception("This class is a singleton!")
        else:
            PriceState._instance = self

    def view_display_message(self, vm):
        self.transition_to(vm, InsertCoinState.instance())
        return 'PRICE ' + VendingMachineState._display_amount(vm.get_display_price())


class SoldOutState(VendingMachineState):
    @staticmethod
    def instance():
        if SoldOutState._instance == None:
            SoldOutState()
        return SoldOutState._instance

    def __init__(self):
        """ Virtually private constructor. """
        if SoldOutState._instance != None:
            raise Exception("This class is a singleton!")
        else:
            SoldOutState._instance = self

    def view_display_message(self, vm):
        if vm.get_balance() == 0:
            self.transition_to(vm, InsertCoinState.instance())
        else:
            self.transition_to(vm, HasCustomerCoinsState.instance())
        return "SOLD OUT"


class ExactChangeOnlyState(VendingMachineState):
    @staticmethod
    def instance():
        if ExactChangeOnlyState._instance == None:
            ExactChangeOnlyState()
        return ExactChangeOnlyState._instance

    def __init__(self):
        """ Virtually private constructor. """
        if ExactChangeOnlyState._instance != None:
            raise Exception("This class is a singleton!")
        else:
            ExactChangeOnlyState._instance = self

    def view_display_message(self, vm):
        return "EXACT CHANGE ONLY"