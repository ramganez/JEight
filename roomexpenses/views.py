import ipdb
import uuid
import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.http import Http404
from django.core import serializers
from django.db.models import Sum

from roomexpenses.forms import AFPFormSet
from roomexpenses.models import MonthExpense, MonthInvestment, RoomMember, IndividualShare

# Create your views here.


def remove_duplicates(obj):
    """get the current month object, remove(set is_deleted=True)
    the other objects from the current model"""

    if isinstance(obj, MonthExpense):
        dub_objs = MonthExpense.objects.filter(created_on__month=obj.created_on.month)
        dub_objs.update(is_deleted=True)
        return True

    elif isinstance(obj, MonthInvestment):
        dub_objs = MonthInvestment.objects.filter(created_on__month=obj.created_on.month)
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
        'Rent': 0, 'Rent-Adjustment':0, 'Food': 0, 'Total': 0,
        }

    if exp_obj and inves_obj:
        data_dict['Month'] = exp_obj.created_on.strftime("%B")
        data_dict['MonthExp'] = exp_obj.get_total_exp()
        data_dict['MonthInves'] = inves_obj.get_total_inves()
        data_dict['Rent'] = exp_obj.rent + exp_obj.maintenance

        data_dict['Rent-Adjustment'] = exp_obj.rent + exp_obj.maintenance - inves_obj.get_total_adjustment()
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

    rent_share = data_dict['Rent-Adjustment'] / rent_share_count
    food_share = data_dict['Food'] / food_share_count
    total_share = data_dict['Total']

    unique_id = uuid.uuid4().hex
    for k, v in individual_choices.iteritems():
        room_mem_obj = RoomMember.objects.get(id=k)
        inves_obj = MonthInvestment.objects.get(is_deleted=False, created_on__month=datetime.datetime.now().month)

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
        return reverse('roomexpenses:month_investment')


class MonthInvestmentCreate(CreateView):

    def form_valid(self, form):
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthinves_obj = form.save(commit=False)
        remove_duplicates(monthinves_obj)

        return super(MonthInvestmentCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MonthInvestmentCreate, self).get_context_data(**kwargs)

        if self.request.POST:
            context['adjusment_formset'] = AFPFormSet(self.request.POST)
        else:
            context['adjusment_formset'] = AFPFormSet()

        context['prev_exp_obj'] = MonthExpense.objects.get(created_on__month=datetime.datetime.now().month,
                                                           is_deleted=False)
        return context

    def post(self, request, *args, **kwargs):
        super(MonthInvestmentCreate, self).post(request, *args, **kwargs)
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


class MonthExpenesUpdate(UpdateView):

    def form_valid(self, form):
        ipdb.set_trace()
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthexp_obj = form.save(commit=False)
        remove_duplicates(monthexp_obj)
        monthexp_obj.save()

        return super(MonthExpenesUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('roomexpenses:month_investment')


class MonthInvestmentUpdate(UpdateView):

    def form_valid(self, form):
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthinves_obj = form.save(commit=False)
        remove_duplicates(monthinves_obj)

        return super(MonthInvestmentUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MonthInvestmentUpdate, self).get_context_data(**kwargs)

        if self.request.POST:
            context['adjusment_formset'] = AFPFormSet(self.request.POST, instance=self.object)
        else:
            context['adjusment_formset'] = AFPFormSet(instance=self.object)

        context['prev_exp_obj'] = MonthExpense.objects.get(created_on__month=datetime.datetime.now().month,
                                                           is_deleted=False)
        return context

    def post(self, request, *args, **kwargs):
        super(MonthInvestmentUpdate, self).post(request, *args, **kwargs)
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
        context.update({'prev_inves_obj': MonthInvestment.objects.get(created_on__month=datetime.datetime.now().month,
                                                                 is_deleted=False)})
        context.update({'action_url': a_url})
        return context

    def get_queryset(self):
        qs = super(PeopleShareList, self).get_queryset()
        result = qs.filter(is_deleted=False)
        return result


def month_share(request):

    if request.method == 'POST':
        try:
            current_exp = MonthExpense.objects.get(created_on__month=datetime.datetime.now().month, is_deleted=False)
        except:
            raise Http404("Month Expense does not exist")

        try:
            current_inves = MonthInvestment.objects.get(created_on__month=datetime.datetime.now().month, is_deleted=False)

        except:
            raise Http404("Month Investment does not exist")

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
        total_indiv_shares = IndividualShare.objects.filter(created_on__month=datetime.datetime.now().month,
                                                            created_on__year=datetime.datetime.now().year,
                                                            is_deleted=False).aggregate(Sum('amount_to_pay'))


        # for showing afp details
        afp_objs = current_inves.adjustmentfrompeople_set.all()

        return render(request, 'roomexpenses/month_share.html', {'indiv_qs':indiv_qs, 'data_dict': data_dict,
                                                                 'afp_objs': afp_objs,
                                                                 'total_indiv_shares':total_indiv_shares})

    else:
        # return render(request, 'roomexpenses/month_share.html')
        return redirect('signin')


def expenses_history(request, **kwargs):
    if request.method == 'GET':

        exp_fields = ('rent', 'maintenance', 'veg_shop',
                      'water', 'EB', 'cable', 'commonEB', 'other')

        inves_fields = ('provision_store', 'gas', 'rice_bag',
                        'new_things')

        try:
            exp_obj= MonthExpense.objects.filter(created_on__month=kwargs['month'],
                                            created_on__year=kwargs['year'], is_deleted=False)

            exp_data = serializers.serialize("python", exp_obj,
                                             fields=exp_fields)[0]
        except:
            exp_data = None

        try:
            inves_obj = MonthInvestment.objects.filter(created_on__month=kwargs['month'],
                                                created_on__year=kwargs['year'], is_deleted=False)
            inves_data = serializers.serialize( "python", inves_obj, fields=inves_fields)[0]

        except:
            inves_data = None

        try:
            indiv_qs = IndividualShare.objects.filter(created_on__month=kwargs['month'],
                                                      created_on__year=kwargs['year'], is_deleted=False)

            total_indiv_shares = IndividualShare.objects.filter(created_on__month=kwargs['month'],
                                                                created_on__year=kwargs['year'],
                                                                is_deleted=False).aggregate(Sum('amount_to_pay'))
        except:
            indiv_qs = None

        # for showing afp details
        try:
            afp_objs = inves_obj[0].adjustmentfrompeople_set.all()
        except:
            afp_objs=None

        context = {'exp_data': exp_data,
                   'exp_obj':exp_obj[0],
                   'inves_data': inves_data,
                   'inves_obj':inves_obj[0],
                   'afp_objs': afp_objs,
                   'indiv_qs': indiv_qs,
                   'total_indiv_shares': total_indiv_shares
                   }
        return render(request, 'roomexpenses/expenses_history.html', context)

    else:
        # fixme later
        return redirect('signin')