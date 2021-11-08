from django import forms
from django.forms import ModelForm
from . models import *


class CreateForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['start_time','end_time', 'participants']
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    participants = forms.ModelMultipleChoiceField(
        queryset=Participant.objects.all(),
        widget=forms.CheckboxSelectMultiple

    )