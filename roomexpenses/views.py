import ipdb

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from roomexpenses.forms import AFPFormSet

# Create your views here.


class MonthExpenesCreate(CreateView):

    def get_success_url(self):
        return reverse('roomexpenses:month_invesment')


class MonthInvesmentCreate(CreateView):

    def get_context_data(self, **kwargs):
        context = super(MonthInvesmentCreate, self).get_context_data(**kwargs)

        if self.request.POST:
            context['adjusment_formset'] = AFPFormSet(self.request.POST)
        else:
            context['adjusment_formset'] = AFPFormSet()

        return context

    def post(self, request, *args, **kwargs):
        super(MonthInvesmentCreate, self).post(request, *args, **kwargs)
        form = self.get_form()
        if form.is_valid():
            inves_obj = form.save()
            context = self.get_context_data(**kwargs)
            adjusment_form = context['adjusment_formset']
            adjusment_form.instance = inves_obj
            if adjusment_form.is_valid():
                adjusment_form.save()

            return self.form_valid(form)

        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('roomexpenses:people_share')


class PeopleShareList(ListView):

    def get_context_data(self, **kwargs):
        context = super(PeopleShareList, self).get_context_data(**kwargs)
        a_url = reverse('roomexpenses:month_share')
        context.update({'action_url': a_url })
        return context

    def get_queryset(self):
        qs = super(PeopleShareList, self).get_queryset()
        result = qs.filter(is_deleted=False)
        return result


def month_share(request):
    if request.POST:
        ipdb.set_trace()
        pass

    return render(request, 'roomexpenses/month_share.html')