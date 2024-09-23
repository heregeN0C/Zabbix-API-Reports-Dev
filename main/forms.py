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

class ReportForm(forms.Form):
    CHOICES = [
        ('opcaoteste', 'OPção Teste')
    ]
    graph_select = forms.CharField()
    date_select = forms.DateField()
    time_select = forms.TimeField()
    date_end_select = forms.DateField()
    time_end_select = forms.TimeField()