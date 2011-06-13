from django import forms
from django.utils.safestring import mark_safe
from globalrequest.middleware import get_request
from .models import Livelihood, Category, Location
from .tools import GeoForm


def categories():
    items = [] 
    for parent in Category.objects.all():
        if parent.ancestor:
            continue
        cats = ()
        for cat in Category.objects.filter(ancestor=parent):
            cats += ((cat.id, cat.name),)
        items.append((parent.name, cats))
    return items

def districts():
    items = []
    for d in Location.objects.filter(parent=0):
        items.append((d.id, d.name))
    return items


class DistrictForm(GeoForm):
    def __init__(self, *args, **kwargs):
        super(DistrictForm, self).__init__(*args, **kwargs)
        self.fields['district'].widget.choices = districts()
        self.fields['sub_district'].widget.choices = [] 
        self.fields['village'].widget.choices = []


class LivelihoodForm(DistrictForm):
    category = forms.fields.MultipleChoiceField()

    class Meta:
        model = Livelihood
        exclude = ('category','cluster_count','group_count','member_count')

    def __init__(self, *args, **kwargs):
        super(LivelihoodForm, self).__init__(*args, **kwargs)
        self.fields['category'].initial = self.instance.category
        self.fields['category'].choices = \
            self.fields['category'].widget.choices = categories()
        self.fields['name'].widget.attrs = {'size': 40}
        self.fields['category'].widget.attrs = {'size': 10}
        self.fields['address'].widget.attrs = {'cols': 40, 'rows': 2}
        self.fields['description'].widget.attrs = {'cols': 40, 'rows': 2}

    def save(self, *args, **kwargs):
        request = get_request()
        self.instance.category = request.POST.getlist('category')
        super(LivelihoodForm, self).save(*args, **kwargs)


