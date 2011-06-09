from django import forms
from .models import Product
from livecenter.forms import GeoForm, categories


class ProductForm(GeoForm):
    class Meta:
        model = Product
        exclude = ('person','livecenter','cluster')
        widgets = {
            'address': forms.Textarea(attrs={'cols': 20, 'rows': 2}),
            'info': forms.Textarea(attrs={'cols': 20, 'rows': 2}),
            }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs = {'size': 10}
        self.fields['category'].widget.choices = categories()

