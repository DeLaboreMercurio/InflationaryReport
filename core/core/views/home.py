from crum import get_current_user
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpRequest
from django.shortcuts import redirect, render
from core.models.balances import Balance
from core.models.transactions import Category, Transaction, TransactionTypes
from core.tables.transactions import CategoryTransactionsTable, TransactionsTable
from core.forms.transactions import NewTransactionForm
from core.forms.categories import NewCategoryForm
from core.views.builders import get_expenses_by_category
from django.contrib import messages

from django.utils.translation import gettext_lazy as _


@login_required()
def home_view(request):

    if request.method == "POST":

        if "new-transaction" in request.POST:
            return _handle_new_transaction(request)

        elif "new-category" in request.POST:
            return _handle_new_category(request)

    return _render_home_view(request)


def _render_home_view(request: HttpRequest) -> HttpRequest:
    """_render_home_view renders the home view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpRequest: The request object
    """
    transactions = Transaction.objects.filter(creator=request.user)
    transactions_table = TransactionsTable(transactions)

    category_totals_table = _generate_transactions_category_forecast_table(request)
    current_balance = Balance.objects.get(user=request.user).total
    transaction_form = NewTransactionForm(
        user=get_current_user(), initial={"type": "OUT", "amount": 0}
    )
    new_category_form = NewCategoryForm()

    outgoing_categories_list, outgoing_totals_list = get_expenses_by_category(
        TransactionTypes.OUTGOING
    )
    incoming_categories_list, incoming_totals_list = get_expenses_by_category(
        TransactionTypes.INCOMING
    )
    return render(
        request,
        "home.html",
        context={
            "new_transaction_form": transaction_form,
            "balance": current_balance,
            "table": transactions_table,
            "new_category_form": new_category_form,
            "outgoing_categories_list": outgoing_categories_list,
            "outgoing_totals_list": outgoing_totals_list,
            "incoming_categories_list": incoming_categories_list,
            "incoming_totals_list": incoming_totals_list,
            "category_totals_table": category_totals_table,
        },
    )


def _handle_new_category(request: HttpRequest) -> HttpRequest:
    """_handle_new_category handles the creation of a new category

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpRequest: The request object
    """

    form = NewCategoryForm(request.POST)
    if form.is_valid():
        category = form.save(get_current_user())
        messages.success(request, _(f"Category {category.name} created."))
        return redirect("home")


def _handle_new_transaction(request: HttpRequest) -> HttpRequest:
    """_handle_new_transaction handles the creation of a new transaction

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpRequest: The request object
    """
    form = NewTransactionForm(get_current_user(), request.POST)
    if form.is_valid():
        messages.add_message(
            request, messages.INFO, _("Transaction logged."), extra_tags="primary"
        )
        transaction = form.save()
        return redirect("home")


def _generate_transactions_category_forecast_table(
    request: HttpRequest,
) -> CategoryTransactionsTable:

    categories = (
        Transaction.objects.filter(creator=request.user)
        .values("category__name")
        .annotate(total=Sum("amount"))
    )

    forecasts = Category.objects.filter(creator=request.user).exclude(
        associated_forecast__isnull=True
    )
    # TODO Change this to a couple of properties in the model.
    for category in categories:
        for forecast in forecasts:
            if category["category__name"] == forecast.name:
                category["forecast"] = (
                    category["total"]
                    + (forecast.associated_forecast.amount / 100) * category["total"]
                )

    category_totals_table = CategoryTransactionsTable(categories)

    return category_totals_table
