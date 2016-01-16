from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView


from roomexpenses.models import MonthExpense, MonthInvestment, RoomMember
from roomexpenses.forms import MonthExpenseForm, MonthInvestmentForm
from roomexpenses.views import (MonthExpenesCreate, MonthInvestmentCreate,
                                PeopleShareList, month_share, expenses_history)

urlpatterns = [
    # Examples:
    # url(r'^$', 'jeight.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', TemplateView.as_view(template_name='roomexpenses/expenses.html'), name='home'),
    url(r'^month-expense/$',
        MonthExpenesCreate.as_view(form_class=MonthExpenseForm,
                                   template_name='roomexpenses/expenses_form.html'), name='month_expense'),

    url(r'^month-investment/$',
        MonthInvestmentCreate.as_view(form_class=MonthInvestmentForm,
                                     template_name='roomexpenses/investment_form.html'), name='month_investment'),

    url(r'^people-share/$',
        PeopleShareList.as_view(template_name='roomexpenses/people_share.html', model=RoomMember), name='people_share'),

    url(r'^month-share/$', month_share, name='month_share'),

    url(r'^expenses-history/(?P<month>[0-9]+)/(?P<year>[0-9]+)$', expenses_history, name='expenses_history'),

]
