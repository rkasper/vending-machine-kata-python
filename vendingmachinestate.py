from abc import abstractmethod


class VendingMachineState:
    @staticmethod
    def _display_amount(amount: int) -> str:
        return '${:,.2f}'.format(amount / 100)

    @abstractmethod
    def view_display_message(self, vm) -> str:
        return ""

    @staticmethod
    def transition_to(vm, next_vm_state):
        vm.set_vm_state(next_vm_state)


class InsertCoinState(VendingMachineState):
    def view_display_message(self, vm):
        return "INSERT COIN"


class HasCustomerCoinsState(VendingMachineState):
    def view_display_message(self, vm):
        return VendingMachineState._display_amount(vm.get_balance())


class ThankYouState(VendingMachineState):
    def view_display_message(self, vm):
        # TODO The following line shouldn't exist. Try removing it after we refactor toward the Singleton pattern.
        vm.set_vm_state_to_insert_coin_state()
        self.transition_to(vm, InsertCoinState())
        return "THANK YOU"


class PriceState(VendingMachineState):
    def view_display_message(self, vm):
        self.transition_to(vm, InsertCoinState())
        return 'PRICE ' + VendingMachineState._display_amount(vm.get_display_price())


class SoldOutState(VendingMachineState):
    def view_display_message(self, vm):
        if vm.get_balance() == 0:
            self.transition_to(vm, InsertCoinState())
        else:
            self.transition_to(vm, HasCustomerCoinsState())
        return "SOLD OUT"


class ExactChangeOnlyState(VendingMachineState):
    def view_display_message(self, vm):
        return "EXACT CHANGE ONLY"