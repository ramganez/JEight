import ipdb

from django.forms import ModelForm, TextInput
from django import forms

from django.forms import inlineformset_factory, BaseInlineFormSet

from roomexpenses.models import *


class MonthExpenseForm(ModelForm):

    class Meta:
        model = MonthExpense
        fields = ['rent', 'maintenance', 'cable',
                  'EB', 'water', 'commonEB',
                  'veg_shop', 'other']

    def __init__(self, *args, **kwargs):
        super(MonthExpenseForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget = TextInput()


class MonthInvestmentForm(ModelForm):

    class Meta:
        model = MonthInvestment
        fields = ['provision_store', 'new_things',
                  'gas', 'rice_bag']

    def __init__(self, *args, **kwargs):
        super(MonthInvestmentForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget = TextInput()

AFPFormSet = inlineformset_factory(MonthInvestment, AdjustmentFromPeople, fields=('people_name', 'amount'),
                                   extra=2, max_num=2)
