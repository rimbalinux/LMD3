from django import forms
from livecenter.models import Cluster, Category
from livecenter.forms import categories
from attachment.tools import PhotoForm


class ClusterForm(PhotoForm):
    class Meta:
        model = Cluster
        widgets = {
            'livecenter': forms.HiddenInput(),
            'info': forms.Textarea(attrs={'cols': 20, 'rows': 2}),
            }

    def __init__(self, *args, **kwargs):
        super(ClusterForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.choices = categories()

