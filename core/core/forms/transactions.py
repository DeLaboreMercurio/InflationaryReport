from django import forms

from core.models.transactions import Transaction, Category, TransactionTypes
from crispy_forms.helper import FormHelper


class NewTransactionForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.fields["category"] = forms.ChoiceField(choices=self._fetch_user_choices())

    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Transaction

    def save(self, commit=True):
        category = Category.objects.get(id=self.cleaned_data["category"])
        transaction = Transaction(
            amount=self.cleaned_data["amount"],
            description=self.cleaned_data["description"],
            type=category.type,
            category=category,
        )
        if commit:
            transaction.save()
        return transaction

    def _fetch_user_choices(self):

        return (
            (
                "Incoming",
                (
                    list(
                        Category.objects.filter(
                            creator=self.user, type=TransactionTypes.INCOMING
                        ).values_list("id", "name")
                    )
                ),
            ),
            (
                "Outgoing",
                (
                    list(
                        Category.objects.filter(
                            creator=self.user, type=TransactionTypes.OUTGOING
                        ).values_list("id", "name")
                    )
                ),
            ),
        )
