from abc import abstractmethod

class IPayController:

    def __init__(self):
    	pass

    @abstractmethod
    def send_money(self, amount, sender, receiver):
        pass