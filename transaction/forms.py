from django import forms
from counter.tools import BaseForm
from .models import Transaction


class TransactionForm(BaseForm):
    class Meta:
        model = Transaction
        widgets = {
            'person': forms.HiddenInput(),
            }
