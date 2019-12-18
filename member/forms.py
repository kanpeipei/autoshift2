from django import forms
from .models import Members


class MembersForm(forms.ModelForm):
    class Meta:
        model = Members
        exclude = ['created_at', 'updated_at']


class MembersModifyForm(forms.ModelForm):
    class Meta:
        model = Members
        exclude = ['partner_number', 'created_at', 'updated_at']


