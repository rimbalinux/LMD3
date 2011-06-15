from django import forms
from group.models import Group
from livecenter.models import Location, Livelihood
from livecenter.forms import DistrictForm
from counter.tools import BaseForm
from .models import People, Training


def groups(lc):
    items = [('','')]
    for group in Group.objects.filter(livecenter=lc):
        items.append((group.id, group.name))
    return items

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
        self.fields['group'].choices = groups(self.instance.livecenter)
        #self.fields['group'].required = False
        #self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.\
        #    filter(livecenter=self.instance.livecenter),
        #    label='Kelompok',
        #    required=False)

class TrainingForm(BaseForm):
    class Meta:
        model = Training
        widgets = {
            'person': forms.HiddenInput(),
            }


