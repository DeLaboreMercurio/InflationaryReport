from venv import create
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from core.models.balances import Balance
from core.views.builders import create_initial_balance
from django.utils.translation import gettext_lazy as _

# Create your forms here.
CLEANR = re.compile(r"<[^>]+>")


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, "", str(raw_html))
    return cleantext


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # Here we move the help text that is usually displayed in the same form, to a tool tip which is way more elegant because Bootstrap handles it when we set those 3 attributes.
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].widget.attrs.update(
                {
                    "data-toggle": "tooltip",
                    "title": cleanhtml(self.fields[fieldname].help_text),
                    "data-placement": "left",
                }
            )
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class BalanceForm(forms.Form):
    balance = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, label="Initial Balance"
    )

    class Meta:
        model = Balance

    def save(self, commit=True):
        balance = self.cleaned_data["balance"]
        if commit:
            create_initial_balance(balance)
        return balance
