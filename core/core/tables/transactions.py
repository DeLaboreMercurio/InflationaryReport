import django_tables2 as tables

from core.models.transactions import Transaction


class TransactionsTable(tables.Table):

    amount = tables.Column()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render_amount(self, value):
        return f"${value:.2f}"

    class Meta:
        model = Transaction
        exclude = ("id", "creator", "updated_at")
        sequence = ("created_at", "amount", "description", "type")
