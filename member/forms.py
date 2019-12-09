from django import forms
from .models import Members


class MembersForm(forms.ModelForm):
    class Meta:
        model = Members
        # fields = ('name', 'age', 'partner_number', 'hourly_pay',)
        exclude = ['created_at', 'updated_at']


