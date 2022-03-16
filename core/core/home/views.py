from crum import get_current_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from core.models.balances import Balance
from core.models.transactions import Transaction
from core.tables.transactions import TransactionsTable
from core.forms.transactions import NewTransactionForm
from core.forms.categories import NewCategoryForm


@login_required()
def home_view(request):

    if request.method == "POST":

        if "new-transaction" in request.POST:
            form = NewTransactionForm(get_current_user(), request.POST)
            if form.is_valid():
                transaction = form.save()
                return redirect("home")

        elif "new-category" in request.POST:
            form = NewCategoryForm(request.POST)
            if form.is_valid():
                category = form.save(get_current_user())
                return redirect("home")

    transactions = Transaction.objects.filter(creator=request.user)
    transactions_table = TransactionsTable(transactions)

    current_balance = Balance.objects.get(user=request.user).total
    transaction_form = NewTransactionForm(
        user=get_current_user(), initial={"type": "OUT", "amount": 0}
    )
    new_category_form = NewCategoryForm()
    return render(
        request,
        "home.html",
        context={
            "new_transaction_form": transaction_form,
            "balance": current_balance,
            "table": transactions_table,
            "new_category_form": new_category_form,
        },
    )
