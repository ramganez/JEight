from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView


from roomexpenses.models import MonthExpense, MonthInvesment, RoomMember
from roomexpenses.forms import MonthExpenseForm, MonthInvesmentForm
from roomexpenses.views import (MonthExpenesCreate, MonthInvesmentCreate,
                                PeopleShareList, month_share)

urlpatterns = [
    # Examples:
    # url(r'^$', 'jeight.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', TemplateView.as_view(template_name='roomexpenses/expenses.html'), name='home'),
    url(r'^month-expense/$',
        MonthExpenesCreate.as_view(form_class=MonthExpenseForm,
                                   template_name='roomexpenses/expenses_form.html'), name='month_expense'),

    url(r'^month-invesment/$',
        MonthInvesmentCreate.as_view(form_class=MonthInvesmentForm,
                                     template_name='roomexpenses/invesment_form.html'), name='month_invesment'),

    url(r'^people-share/$',
        PeopleShareList.as_view(template_name='roomexpenses/people_share.html', model=RoomMember), name='people_share'),

    url(r'^month-share/$', month_share, name='month_share'),

]
