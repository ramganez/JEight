from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView


from roomexpenses.models import MonthExpense, MonthInvestment, RoomMember
from roomexpenses.forms import MonthExpenseForm, MonthInvestmentForm
from roomexpenses.views import (MonthExpenesCreate, MonthExpenesUpdate,
                                MonthInvestmentCreate, MonthInvestmentUpdate,
                                PeopleShareList, month_share, expenses_history,
                                checklist_calc, get_checklist)

urlpatterns = [
    # Examples:
    # url(r'^$', 'jeight.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', TemplateView.as_view(template_name='roomexpenses/expenses.html'), name='home'),
    url(r'^month-expense/$',
        MonthExpenesCreate.as_view(form_class=MonthExpenseForm,
                                   template_name='roomexpenses/expenses_form.html'), name='month_expense'),

    url(r'^month-expense/update/(?P<pk>[0-9]+)/$',
        MonthExpenesUpdate.as_view(form_class=MonthExpenseForm, model=MonthExpense,
                                   template_name='roomexpenses/expenses_form.html'), name='month_expense_update'),

    url(r'^month-investment/$',
        MonthInvestmentCreate.as_view(form_class=MonthInvestmentForm,
                                      template_name='roomexpenses/investment_form.html'), name='month_investment'),

    url(r'^month-investment/update/(?P<pk>[0-9]+)/$',
        MonthInvestmentUpdate.as_view(form_class=MonthInvestmentForm, model=MonthInvestment,
                                      template_name='roomexpenses/investment_form.html'), name='month_investment_update'),

    url(r'^people-share/$',
        PeopleShareList.as_view(template_name='roomexpenses/people_share.html', model=RoomMember), name='people_share'),

    url(r'^month-share/$', month_share, name='month_share'),

    url(r'^expenses-history/(?P<month>[0-9]+)/(?P<year>[0-9]+)$', expenses_history, name='expenses_history'),

    url(r'^checklist/(?P<month>[0-9]+)/(?P<year>[0-9]+)$', checklist_calc, name='checklist_calc'),

    url(r'^get_checklist/(?P<month>[0-9]+)/(?P<year>[0-9]+)$', get_checklist, name='get_checklist'),
]
