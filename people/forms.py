from django import forms
from .models import People
from group.models import Group
from livecenter.models import Location, Livelihood
from livecenter.tools import GeoForm


class PeopleForm(GeoForm):
    district = forms.ModelChoiceField(queryset=Location.objects.\
            filter(parent=0).order_by('name'))
    sub_district = forms.ModelChoiceField(queryset=Location.objects.\
            filter(parent=-1))
    village = forms.ModelChoiceField(queryset=Location.objects.\
            filter(parent=-1))
    photo = forms.FileField()

    class Meta:
        model = People
        widgets = {
            'livecenter': forms.HiddenInput(),
            'cluster': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'cols': 20, 'rows': 2}),
            'info': forms.Textarea(attrs={'cols': 20, 'rows': 2}),
            }

    def __init__(self, livecenter=None, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        if livecenter:
            lc = livecenter
        else:
            lc = self.instance.livecenter
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.\
            filter(livecenter=lc))
