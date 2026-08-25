from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    """Form used for both creating and updating an Expense."""

    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is None:
            raise forms.ValidationError("Amount cannot be empty.")
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return amount
