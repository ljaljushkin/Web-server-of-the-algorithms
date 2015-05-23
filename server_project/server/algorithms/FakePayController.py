from algorithms.IPayController import IPayController
from algorithms.models import User


class FakePayController(IPayController):
    def __init__(self):
        IPayController.__init__(self)

    def send_money(self, amount, sender, receiver):
        try:
            sender_db = User.objects.filter(login=sender).get()

            if sender_db.account_cash < amount:
                return False

            sender_db.account_cash = sender_db.account_cash - amount
            sender_db.save()

            receiver_db = User.objects.filter(login=receiver).get()

            receiver_db.account_cash = receiver_db.account_cash + amount
            receiver_db.save()

            return True

        except User.DoesNotExist:
            return False
