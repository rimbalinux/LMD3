import datetime
from django import forms
from livecenter.tools import GeoForm
from livecenter.models import Cluster
from counter.tools import BaseForm
from .models import Group, Report, Training


def clusters(lc):
    items = [('','')]
    for cluster in Cluster.objects.filter(livecenter=lc):
        items.append((cluster.id, cluster.name))
    return items


class GroupForm(GeoForm):
    class Meta:
        model = Group
        exclude = ('member_count',)
        widgets = {
            'livecenter': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'size': 40}),
            'info': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            }

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['cluster'].choices = clusters(self.instance.livecenter)


class ReportForm(BaseForm):
    class Meta:
        model = Report
        widgets = {
            'group': forms.HiddenInput(),
            'cluster': forms.HiddenInput(),
            'livecenter': forms.HiddenInput(),
            }


class TrainingForm(BaseForm):
    class Meta:
        model = Training
        widgets = {
            'group': forms.HiddenInput(),
            'livecenter': forms.HiddenInput(),
            }
            
