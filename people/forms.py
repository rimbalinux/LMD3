from django import forms
from .models import People
from group.models import Group
from livecenter.models import Location, Livelihood
from livecenter.forms import DistrictForm



class PeopleForm(DistrictForm):
    class Meta:
        model = People
        widgets = {
            'livecenter': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'cols': 20, 'rows': 2}),
            'info': forms.Textarea(attrs={'cols': 20, 'rows': 2}),
            }

    def __init__(self, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        self.fields['gender'].initial = True # default male
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.\
            filter(livecenter=self.instance.livecenter),
            label='Kelompok')
