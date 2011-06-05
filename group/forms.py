from django import forms
from livecenter.tools import GeoForm
from .models import Group


class GroupForm(GeoForm):
    class Meta:
        model = Group
        widgets = {
            'livecenter': forms.HiddenInput(),
            'cluster': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'size': 40}),
            'info': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            }

