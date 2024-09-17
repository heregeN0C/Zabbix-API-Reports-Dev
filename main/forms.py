from django import forms

class GroupForm(forms.Form):
    CHOICES = [
        ('opcaoteste', 'OPção Teste')
    ]
    group_select = forms.CharField(required=True)

class HostForm(forms.Form):
    CHOICES = [
        ('opcaoteste', 'OPção Teste')
    ]
    host_select = forms.CharField(required=True)