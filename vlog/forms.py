from django import forms
from vlog.models import Record
from mailing_list.forms import StyleFormMixin


class RecordForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Record
        fields = ('title', 'slug', 'content', 'preview')
