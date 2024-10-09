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

    graph_select = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])
    date_select = forms.CharField()
    time_select = forms.CharField()
    date_end_select = forms.CharField()
    time_end_select = forms.CharField()