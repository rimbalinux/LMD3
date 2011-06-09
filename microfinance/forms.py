from django import forms
from livecenter.tools import GeoForm
from .models import Finance


class FinanceForm(GeoForm):
    class Meta:
        model = Finance

    def __init__(self, *args, **kwargs):
        super(FinanceForm, self).__init__(*args, **kwargs)
        self.fields['name_org'].widget.attrs = {'size': 30}
        self.fields['contact_name'].widget.attrs = {'size': 30}
        self.fields['address'].widget.attrs = {'size': 30}
        self.fields['manajemen_usaha'].widget.attrs = {'size': 5}
        self.fields['pembukuan'].widget.attrs = {'size': 5}
        self.fields['akses_pasar'].widget.attrs = {'size': 5}
        self.fields['keuangan_mikro'].widget.attrs = {'size': 5}
        self.fields['jangka_wkt_pinjaman'].widget.attrs = {'size': 5}
        self.fields['margin_bunga'].widget.attrs = {'size': 5}
        self.fields['ao'].widget.attrs = {'size': 5}
        self.fields['cs'].widget.attrs = {'size': 5}
        self.fields['tl'].widget.attrs = {'size': 5}
        self.fields['kelayakan_usaha'].widget.attrs = {'size': 5}
