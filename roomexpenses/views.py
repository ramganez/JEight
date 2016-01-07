import ipdb
import uuid
import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.http import Http404

from roomexpenses.forms import AFPFormSet
from roomexpenses.models import MonthExpense, MonthInvesment, RoomMember, IndividualShare

# Create your views here.


def remove_duplicates(obj):
    """get the current month object, remove(set is_deleted=True)
    the other objects from the current model"""

    if isinstance(obj, MonthExpense):
        dub_objs = MonthExpense.objects.filter(created_on__month=obj.created_on.month)
        dub_objs.update(is_deleted=True)
        return True

    elif isinstance(obj, MonthInvesment):
        dub_objs = MonthInvesment.objects.filter(created_on__month=obj.created_on.month)
        dub_objs.update(is_deleted=True)
        return True


def create_month_share(exp_obj=None, inves_obj=None):

    """Calculate the TotalExpense(Food+Rent) of given Month and separate the Rent and Food Exp"""

    def get_food_exp(exp_obj, inves_obj):
        return (exp_obj.cable + exp_obj.EB + exp_obj.water + exp_obj.commonEB + exp_obj.veg_shop +
                exp_obj.other + inves_obj.provision_store + inves_obj.gas + inves_obj.rice_bag +
                inves_obj.new_things
                )
    data_dict = {
        'Month': '', 'MonthExp': 0, 'MonthInves': 0,
        'Rent': 0, 'Food': 0, 'Total': 0,
        }

    if exp_obj and inves_obj:
        data_dict['Month'] = exp_obj.created_on.strftime("%B")
        data_dict['MonthExp'] = exp_obj.get_total_exp()
        data_dict['MonthInves'] = inves_obj.get_total_inves()
        data_dict['Rent'] = exp_obj.rent + exp_obj.maintenance
        data_dict['Food'] = get_food_exp(exp_obj, inves_obj)
        data_dict['Total'] = exp_obj.get_total_exp() + inves_obj.get_total_inves()
        return data_dict

    else:
        return data_dict


def create_individual_shares(data_dict=None, individual_choices=None):
    rent_share_count = 0
    food_share_count = 0
    for v in individual_choices.values():
        if '1' in v:
            rent_share_count += 1
        if '2' in v:
            food_share_count += 1

    rent_share = data_dict['Rent'] / rent_share_count
    food_share = data_dict['Food'] / food_share_count
    total_share = data_dict['Total']

    unique_id = uuid.uuid4().hex
    for k, v in individual_choices.iteritems():
        room_mem_obj = RoomMember.objects.get(id=k)
        inves_obj = MonthInvesment.objects.get(is_deleted=False, created_on__month=datetime.datetime.now().month)

        # fixme its needed??
        afp_obj = inves_obj.adjustmentfrompeople_set.all()

        indiv_share_obj = IndividualShare(fk_room_member=room_mem_obj, set_unique_no=unique_id)
        remove_duplicates(indiv_share_obj)
        if '1' in individual_choices[k] and '2' in individual_choices[k]:
            indiv_share_obj.shared = 0
            indiv_share_obj.amount_to_pay = rent_share + food_share

        elif '1' in individual_choices[k]:
            indiv_share_obj.shared = 1
            indiv_share_obj.amount_to_pay = rent_share

        elif '2' in individual_choices[k]:
            indiv_share_obj.shared = 2
            indiv_share_obj.amount_to_pay = food_share

        indiv_share_obj.save()

    dub_objs = IndividualShare.objects.filter(created_on__month=datetime.datetime.now().month).exclude(
            set_unique_no=unique_id)
    dub_objs.update(is_deleted=True)
    return data_dict


class MonthExpenesCreate(CreateView):

    def form_valid(self, form):
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthexp_obj = form.save(commit=False)
        remove_duplicates(monthexp_obj)
        monthexp_obj.save()

        return super(MonthExpenesCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('roomexpenses:month_invesment')


class MonthInvesmentCreate(CreateView):

    def form_valid(self, form):
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthinves_obj = form.save(commit=False)
        remove_duplicates(monthinves_obj)

        return super(MonthInvesmentCreate, self).form_valid(form)

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
        try:
            current_exp = MonthExpense.objects.get(created_on__month=datetime.datetime.now().month, is_deleted=False)
        except:
            raise Http404("Month Expense does not exist")

        try:
            current_inves = MonthInvesment.objects.get(created_on__month=datetime.datetime.now().month, is_deleted=False)
        except:
            raise Http404("Month Invesment does not exist")

        data_dict = create_month_share(exp_obj=current_exp, inves_obj=current_inves)

        # create share for individual
        individual_choices = {}
        for key, value in request.POST.iteritems():
            try:
                individual_choices[int(key)] = request.POST.getlist(key)
            except:
                continue

        data_dict = create_individual_shares(data_dict, individual_choices)
        indiv_qs = IndividualShare.objects.filter(created_on__month=datetime.datetime.now().month, is_deleted=False)

        return render(request, 'roomexpenses/month_share.html', {'indiv_qs':indiv_qs, 'data_dict': data_dict})

    else:
        # return render(request, 'roomexpenses/month_share.html')
        return redirect('signin')