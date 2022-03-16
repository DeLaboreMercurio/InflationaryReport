from core.models.balances import Balance

from crum import get_current_user


def create_initial_balance(balance: float = 0):

    balance = Balance.objects.create(total=balance, user=get_current_user())
