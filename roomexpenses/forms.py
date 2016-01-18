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

# not required
# class CustomInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super(CustomInlineFormSet, self).clean()
#         # example custom validation across forms in the formset
#         for form in self.forms:
#             # your custom formset validation
#             data = form.cleaned_data
#
#             if not data:
#                 raise forms.ValidationError("Please enter the name")
#             return data

AFPFormSet = inlineformset_factory(MonthInvestment, AdjustmentFromPeople, fields=('people_name', 'amount'),
                                   extra=2, max_num=2)
