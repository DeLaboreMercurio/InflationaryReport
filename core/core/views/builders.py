from typing import Tuple
from core.models.balances import Balance
from core.models.transactions import Category, Transaction, TransactionTypes

from crum import get_current_user
from django.db.models import Sum


def create_initial_balance(balance: float = 0):

    balance = Balance.objects.create(total=balance, user=get_current_user())

def get_expenses_by_category(transaction_type: TransactionTypes) -> Tuple[list, list]:
    """get_expenses_by_category returns a list of tuples with the category name and the total amount of expenses in that category

    Args:
        transaction_type (TransactionTypes): The type of transaction to filter by

    Returns:
        Tuple[list, list]: A list of tuples with the category name and the total amount of expenses in that category
    """    

    user = get_current_user()

    categories_list = []
    totals_list = []

    for category in Category.objects.filter(type=transaction_type, creator=user):
        
        expenses = Transaction.objects.filter(category=category, creator=user).aggregate(Sum('amount'))['amount__sum']
        if expenses is not None and expenses > 0:
            categories_list.append(category.name)
            totals_list.append(int(expenses))
    
    return categories_list, totals_list





