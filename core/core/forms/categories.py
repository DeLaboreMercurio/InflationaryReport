from django import forms
from core.models.transactions import Category, TransactionTypes


class NewCategoryForm(forms.ModelForm):

    starting_type = (TransactionTypes.STARTING.value, TransactionTypes.STARTING.label)
    choices = TransactionTypes.choices
    choices.remove(starting_type)
    type = forms.ChoiceField(choices=choices)

    class Meta:
        model = Category
        fields = ["name", "associated_forecast"]

    def save(self, user, commit=True):
        category = Category(
            name=self.cleaned_data["name"], creator=user, type=self.cleaned_data["type"], associated_forecast=self.cleaned_data["associated_forecast"]
        )
        if commit:
            category.save()
        return category
