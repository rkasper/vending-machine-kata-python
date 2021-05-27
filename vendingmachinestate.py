from abc import abstractmethod


class VendingMachineState:
    @staticmethod
    def _display_amount(amount: int) -> str:
        return '${:,.2f}'.format(amount / 100)

    @abstractmethod
    def view_display_message(self, vm) -> str:
        return ""


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
        vm.set_vm_state(InsertCoinState())
        return 'PRICE ' + VendingMachineState._display_amount(vm.get_display_price())


class SoldOutState(VendingMachineState):
    def view_display_message(self, vm):
        if vm.get_balance() == 0:
            vm.set_vm_state(InsertCoinState())
        else:
            vm.set_vm_state(HasCustomerCoinsState())
        return "SOLD OUT"


class ExactChangeOnlyState(VendingMachineState):
    def view_display_message(self, vm):
        return "EXACT CHANGE ONLY"