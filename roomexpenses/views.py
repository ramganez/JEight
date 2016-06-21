import ipdb
import uuid
import datetime
from dateutil.relativedelta import relativedelta
import simplejson

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.http import Http404, HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist

from roomexpenses.forms import AFPFormSet, MonthExpenseForm, MonthInvestmentForm
from roomexpenses.models import MonthExpense, MonthInvestment, RoomMember, IndividualShare
from account.views import LoginRequiredMixin

# Create your views here.


def remove_duplicates(obj, is_paid=False):
    """get the current month object, remove(set is_deleted=True)
    the other objects from the current model"""

    if isinstance(obj, MonthExpense):
        dub_objs = MonthExpense.objects.filter(created_on__month=obj.created_on.month,
                                               created_on__year=obj.created_on.year, is_paid=is_paid)
        dub_objs.update(is_deleted=True)
        return True

    elif isinstance(obj, MonthInvestment):
        dub_objs = MonthInvestment.objects.filter(created_on__month=obj.created_on.month,
                                                  created_on__year=obj.created_on.year, is_paid=is_paid)
        dub_objs.update(is_deleted=True)
        return True


def remove_indiv_duplicates(created_on=None, is_paid=False):
    """get the current month object, remove(set is_deleted=True)
    the other objects from the current model"""

    dub_objs = IndividualShare.objects.filter(created_on__month=created_on.month, is_paid=is_paid,
                                              created_on__year=created_on.year)
    dub_objs.update(is_deleted=True)
    return True



def get_next_month(this_month, this_year):
    # day no need to mention by default 1
    this_datetime = datetime.datetime(month=int(this_month), year=int(this_year), day=1)
    return this_datetime + relativedelta(months=1)


def get_prev_month(this_month, this_year):
    # day no need to mention by default 1
    this_datetime = datetime.datetime(month=int(this_month), year=int(this_year), day=1)
    return this_datetime - relativedelta(months=1)


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
        inves_obj = MonthInvestment.objects.get(is_deleted=False, created_on__month=datetime.datetime.now().month,
                                                is_paid=False)

        # fixme its needed??
        afp_obj = inves_obj.adjustmentfrompeople_set.all()

        indiv_share_obj = IndividualShare(fk_room_member=room_mem_obj, set_unique_no=unique_id)
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

    return data_dict


class MonthExpenesCreate(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthexp_obj = form.save(commit=False)
        remove_duplicates(monthexp_obj)
        # if have
        remove_duplicates(monthexp_obj, is_paid=True)
        monthexp_obj.save()

        return super(MonthExpenesCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('roomexpenses:month_investment')


class MonthInvestmentCreate(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthinves_obj = form.save(commit=False)
        remove_duplicates(monthinves_obj)
        # if have
        remove_duplicates(monthinves_obj, is_paid=True)

        return super(MonthInvestmentCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MonthInvestmentCreate, self).get_context_data(**kwargs)

        if self.request.POST:
            context['adjusment_formset'] = AFPFormSet(self.request.POST)
        else:
            context['adjusment_formset'] = AFPFormSet()

        context['prev_exp_obj'] = MonthExpense.objects.get(created_on__month=datetime.datetime.now().month,
                                                           is_deleted=False, is_paid=False)
        return context

    def post(self, request, *args, **kwargs):
        # ipdb.set_trace()
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


class MonthExpenesUpdate(LoginRequiredMixin, UpdateView):

    def form_valid(self, form):
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthexp_obj = form.save(commit=False)
        remove_duplicates(monthexp_obj)
        # if have
        remove_duplicates(monthexp_obj, is_paid=True)
        monthexp_obj.save()

        return super(MonthExpenesUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('roomexpenses:month_investment')


class MonthInvestmentUpdate(LoginRequiredMixin, UpdateView):

    def form_valid(self, form):
        """
        If the form is valid, save the associated model. and remove duplicates
        """
        monthinves_obj = form.save(commit=False)
        remove_duplicates(monthinves_obj)
        # if have
        remove_duplicates(monthinves_obj, is_paid=True)

        return super(MonthInvestmentUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MonthInvestmentUpdate, self).get_context_data(**kwargs)

        if self.request.POST:
            context['adjusment_formset'] = AFPFormSet(self.request.POST, instance=self.object)
        else:
            context['adjusment_formset'] = AFPFormSet(instance=self.object)

        context['prev_exp_obj'] = MonthExpense.objects.get(created_on__month=datetime.datetime.now().month,
                                                           is_deleted=False, is_paid=False)
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


class PeopleShareList(LoginRequiredMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(PeopleShareList, self).get_context_data(**kwargs)
        a_url = reverse('roomexpenses:month_share')
        context.update({'prev_inves_obj': MonthInvestment.objects.get(created_on__month=datetime.datetime.now().month,
                                                                 is_deleted=False, is_paid=False)})
        context.update({'action_url': a_url})
        return context

    def get_queryset(self):
        qs = super(PeopleShareList, self).get_queryset()
        result = qs.filter(is_deleted=False)
        return result


@login_required
def month_share(request):

    if request.method == 'POST':
        try:
            current_exp = MonthExpense.objects.get(created_on__month=datetime.datetime.now().month, is_deleted=False,
                                                   is_paid=False)
        except:
            raise Http404("Month Expense does not exist")

        try:
            current_inves = MonthInvestment.objects.get(created_on__month=datetime.datetime.now().month,
                                                        is_deleted=False, is_paid=False)

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

        remove_indiv_duplicates(created_on=datetime.datetime.now())
        remove_indiv_duplicates(created_on=datetime.datetime.now(), is_paid=True)

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

@login_required
def expenses_history(request, **kwargs):
    # import ipdb;ipdb.set_trace()
    prev_month = get_prev_month(kwargs['month'], kwargs['year'])
    prev_history_url = reverse('roomexpenses:expenses_history', kwargs={'month': prev_month.month,
                                                                        'year': prev_month.year})

    next_month = get_next_month(kwargs['month'], kwargs['year'])
    next_history_url = reverse('roomexpenses:expenses_history', kwargs={'month': next_month.month,
                                                                        'year': next_month.year})

    if request.method == 'GET':

        exp_fields = ('rent', 'maintenance', 'veg_shop',
                      'water', 'EB', 'cable', 'commonEB', 'other')

        inves_fields = ('provision_store', 'gas', 'rice_bag',
                        'new_things')

        try:
            exp_qs = MonthExpense.objects.filter(created_on__month=kwargs['month'],
                                                 created_on__year=kwargs['year'], is_deleted=False, is_paid=False)
            exp_obj = exp_qs[0]
            exp_data = serializers.serialize("python", exp_qs,
                                             fields=exp_fields)[0]
            exp_data_form = MonthExpenseForm(instance=exp_obj, prefix='monthexp')

        except:
            exp_data = None
            exp_obj = None
            exp_data_form = None

        try:
            inves_qs = MonthInvestment.objects.filter(created_on__month=kwargs['month'],
                                                created_on__year=kwargs['year'], is_deleted=False, is_paid=False)
            inves_obj = inves_qs[0]
            inves_data = serializers.serialize("python", inves_qs, fields=inves_fields)[0]

            inves_data_form = MonthInvestmentForm(instance=inves_obj, prefix='monthinves')

        except:
            inves_data = None
            inves_obj = None
            inves_data_form = None

        try:
            indiv_qs = IndividualShare.objects.filter(created_on__month=kwargs['month'],
                                                      created_on__year=kwargs['year'], is_deleted=False, is_paid=False)

            total_indiv_shares = IndividualShare.objects.filter(created_on__month=kwargs['month'],
                                                                created_on__year=kwargs['year'],
                                                                is_deleted=False,
                                                                is_paid=False).aggregate(Sum('amount_to_pay'))
        except:
            indiv_qs = None
            total_indiv_shares = None

        # for showing afp details
        try:
            adjusment_formset = AFPFormSet(instance=inves_obj)
            afp_objs = inves_obj.adjustmentfrompeople_set.all()
        except:
            adjusment_formset = None
            afp_objs = None

        checklist_available = False
        get_checklist_url = ''
        # confirm with one table is enough
        # if checklist available show the prev checklist form else show form with original value
        exp_obj_paid = MonthExpense.objects.filter(created_on__month=kwargs['month'],
                                              created_on__year=kwargs['year'], is_deleted=False, is_paid=True)
        if exp_obj_paid:
            checklist_available = True
            get_checklist_url = reverse('roomexpenses:get_checklist', kwargs={'month': int(kwargs['month']),
                                                                              'year': int(kwargs['year']),})

        # if exp_obj or inves_obj:
        #     # checklist enable only for last month
        #     current_month_year = datetime.datetime.now().month, datetime.datetime.now().year
        #     last_month_year = get_prev_month(*current_month_year).month, get_prev_month(*current_month_year).year
        #     selected_month_year = int(kwargs['month']), int(kwargs['year'])

            # if last_month_year == selected_month_year:
            #     checklist_enable = True

        context = {'exp_data_form': exp_data_form,
                   'exp_obj': exp_obj,
                   'inves_data_form': inves_data_form,
                   'inves_obj': inves_obj,
                   'adjusment_formset': adjusment_formset,
                   'afp_objs': afp_objs,
                   'indiv_qs': indiv_qs,
                   'total_indiv_shares': total_indiv_shares,
                   'prev_history_url': prev_history_url,
                   'next_history_url': next_history_url,
                   'this_month': int(kwargs['month']),
                   'this_year': int(kwargs['year']),
                   'checklist_available': checklist_available,
                   'checklist_url': reverse('roomexpenses:checklist_calc', kwargs={
                       'month': int(kwargs['month']),
                       'year': int(kwargs['year']),
                        }),
                   'get_checklist_url': get_checklist_url,
                   }
        return render(request, 'roomexpenses/expenses_history.html', context)

    else:
        # fixme later
        return redirect('signin')


# create json object with result data
def create_checklist_data(data_dict=None, monthexp_form=None, monthexp_obj=None,
                          monthinves_form=None, monthinves_obj=None, adjusment_set=None):
    # for expense
    exp_fields = monthexp_form.fields.keys()
    exp_obj_dict = simplejson.loads(serializers.serialize('json', [monthexp_obj, ]))[0]['fields']

    for e in exp_fields:
        data_dict['expense'].append(exp_obj_dict[e])

    # for investment
    inves_fields = monthinves_form.fields.keys()
    inves_obj_dict = simplejson.loads(serializers.serialize('json', [monthinves_obj, ]))[0]['fields']

    for e in inves_fields:
        data_dict['investment'].append(inves_obj_dict[e])

    # for afp
    if adjusment_set:
        for e in adjusment_set:
            data_dict['afp'].append(e.amount)

    return data_dict


def get_checklist_result(created_on=None):
    # import ipdb;ipdb.set_trace()
    if created_on:
        monthexp_obj = MonthExpense.objects.get(is_deleted=False, is_paid=False, created_on__month=created_on.month,
                                                created_on__year=created_on.year)

        monthexp_paid_obj = MonthExpense.objects.get(is_deleted=False, is_paid=True, created_on__month=created_on.month,
                                                     created_on__year=created_on.year)

        monthexp_diff = monthexp_paid_obj.get_total_exp() - monthexp_obj.get_total_exp()

        monthinves_obj = MonthInvestment.objects.get(is_deleted=False, is_paid=False,
                                                     created_on__month=created_on.month,
                                                     created_on__year=created_on.year)

        monthinves_paid_obj = MonthInvestment.objects.get(is_deleted=False, is_paid=True,
                                                          created_on__month=created_on.month,
                                                          created_on__year=created_on.year)

        monthinves_diff = monthinves_paid_obj.get_total_inves() - monthinves_obj.get_total_inves()

        afp_diff = monthinves_paid_obj.get_total_adjustment() - monthinves_obj.get_total_adjustment()

        indiv_qs = IndividualShare.objects.filter(created_on__month=created_on.month,
                                                  created_on__year=created_on.year, is_paid=False, is_deleted=False)
        # total_indiv = reduce((lambda x,y: x+y), indiv_qs)
        total_indiv = indiv_qs.aggregate(Sum('amount_to_pay'))

        indiv_paid_qs = IndividualShare.objects.filter(created_on__month=created_on.month,
                                                       created_on__year=created_on.year, is_paid=True,
                                                       is_deleted=False)
        # total_indiv_paid = reduce((lambda x,y: x+y), indiv_paid_qs)
        total_indiv_paid = indiv_paid_qs.aggregate(Sum('amount_to_pay'))

        indiv_share_diff = total_indiv_paid['amount_to_pay__sum'] - total_indiv['amount_to_pay__sum']

        result = monthexp_diff + monthinves_diff + afp_diff + indiv_share_diff

        if result >= 0:
            return "We have {}Rs in our hand".format(result)
        else:
            return "We have to add {}Rs to next month".format(result)


def create_paid_indiv_obj(id=None, amount=None):
    indiv_obj = get_object_or_404(IndividualShare, pk=id)
    indiv_obj.pk = None

    # clone new paid obj from original
    indiv_obj.amount_to_pay = amount
    indiv_obj.is_paid = True
    indiv_obj.save()

    return indiv_obj


@login_required
def checklist_calc(request, **kwargs):
    import ipdb;ipdb.set_trace()
    try:
        monthexp_obj = MonthExpense.objects.get(is_deleted=False, is_paid=False, created_on__month=kwargs['month'],
                                                   created_on__year=kwargs['year'])

        monthinves_obj = MonthInvestment.objects.get(is_deleted=False, is_paid=False, created_on__month=kwargs['month'],
                                                   created_on__year=kwargs['year'])
    except MonthExpense.DoesNotExist:
        raise Http404("Month Expense does not exist")

    except MonthInvestment.DoesNotExist:
        raise Http404("Month Investment does not exist")

    monthexp_form = MonthExpenseForm(request.POST, prefix="monthexp")
    monthinves_form = MonthInvestmentForm(request.POST, prefix="monthinves")

    error_dict = {'monthexp': None,
                  'monthinves': None,
                  'afp': None,
                  }

    if request.is_ajax():
        if monthexp_form.is_valid() and monthinves_form.is_valid():

            expen_obj = monthexp_form.save(commit=False)
            inves_obj = monthinves_form.save(commit=False)

            expen_obj.is_paid = True
            expen_obj.created_on = monthexp_obj.created_on
            inves_obj.is_paid = True
            inves_obj.created_on = monthinves_obj.created_on
            remove_duplicates(expen_obj, is_paid=True)
            expen_obj.save()
            remove_duplicates(inves_obj, is_paid=True)
            inves_obj.save()

            if monthinves_obj.adjustmentfrompeople_set.all():
                adjusment_formset = AFPFormSet(request.POST)
                adjusment_formset.instance = inves_obj
                if adjusment_formset.is_valid():
                    adjusment_set = adjusment_formset.save(commit=False)
                    for adjusment_obj in adjusment_set:
                        adjusment_obj.is_paid = True
                        adjusment_obj.created_on = monthinves_obj.created_on
                        adjusment_obj.save()
                else:
                    # before render the errors , create is_paid object with paid 0 value for adjusment_obj and indiv_objs
                    adjusment_set = monthinves_obj.adjustmentfrompeople_set.all()
                    for adjusment_obj in adjusment_set:
                        from roomexpenses.models import AdjustmentFromPeople
                        AdjustmentFromPeople.objects.create(fk_investment=inves_obj, is_paid=True, amount=0,
                                                    created_on=monthinves_obj.created_on)

                    # add is_paid values in IndividualShare objects
                    input_names = [name for name in request.POST.keys() if name.startswith('indivobj')]
                    indiv_fields = [tuple(i.split('_')) for i in input_names]

                    remove_indiv_duplicates(created_on=monthexp_obj.created_on, is_paid=True)
                    for each in indiv_fields:
                        amount = request.POST['_'.join(each)]
                        indiv_obj = create_paid_indiv_obj(id=each[1], amount=amount)
                        unique_id = indiv_obj.set_unique_no

                    error_dict['afp'] = adjusment_formset.errors
                    return JsonResponse(error_dict, status=400)
            else:
                adjusment_set = None

            # add is_paid values in IndividualShare objects
            input_names = [name for name in request.POST.keys() if name.startswith('indivobj')]
            indiv_fields = [tuple(i.split('_')) for i in input_names]

            data_dict = {'expense': [],
                         'investment': [],
                         'afp': [],
                         'individual_share': [],
                         }

            remove_indiv_duplicates(created_on=monthexp_obj.created_on, is_paid=True)
            for each in indiv_fields:
                amount = request.POST['_'.join(each)]
                indiv_obj = create_paid_indiv_obj(id=each[1], amount=amount)
                data_dict['individual_share'].append(indiv_obj.amount_to_pay)
                unique_id = indiv_obj.set_unique_no

            result_str = get_checklist_result(created_on=monthexp_obj.created_on)

            get_checklist_url = reverse('roomexpenses:get_checklist', kwargs={'month': int(kwargs['month']),
                                                                              'year': int(kwargs['year']),})



            result_dict = create_checklist_data(data_dict=data_dict,
                                                monthexp_form=monthexp_form, monthexp_obj=expen_obj,
                                                monthinves_form=monthinves_form, monthinves_obj=inves_obj,
                                                adjusment_set=adjusment_set,)
            result_dict['result_str'] = result_str
            result_dict['get_checklist_url'] = get_checklist_url

            return JsonResponse(result_dict)

        else:
            error_dict['monthexp'] = monthexp_form.errors.keys()
            error_dict['monthinves'] = monthinves_form.errors.keys()
            return JsonResponse(error_dict, status=400)


def get_checklist(request, **kwargs):
    # import ipdb;ipdb.set_trace()
    try:
        monthexp_obj = MonthExpense.objects.get(is_deleted=False, is_paid=True, created_on__month=kwargs['month'],
                                                   created_on__year=kwargs['year'])

        monthinves_obj = MonthInvestment.objects.get(is_deleted=False, is_paid=True, created_on__month=kwargs['month'],
                                                   created_on__year=kwargs['year'])

    except MonthExpense.DoesNotExist:
        raise Http404("Month Expense does not exist")

    except MonthInvestment.DoesNotExist:
        raise Http404("Month Investment does not exist")

    if request.is_ajax():
        data_dict = {'expense': [],
                     'investment': [],
                     'afp': [],
                     'individual_share': [],
                     }

        indiv_qs = IndividualShare.objects.filter(is_deleted=False, is_paid=True, created_on__month=kwargs['month'],
                                    created_on__year=kwargs['year'])
        for each in indiv_qs:
            amount = each.amount_to_pay
            data_dict['individual_share'].append(amount)

        monthexp_form = MonthExpenseForm(request.POST, prefix="monthexp")
        monthinves_form = MonthInvestmentForm(request.POST, prefix="monthinves")


        result_str = get_checklist_result(created_on=monthexp_obj.created_on)
        result_dict = create_checklist_data(data_dict=data_dict,
                                            monthexp_form=monthexp_form, monthexp_obj=monthexp_obj,
                                            monthinves_form=monthinves_form, monthinves_obj=monthinves_obj,
                                            adjusment_set=monthinves_obj.adjustmentfrompeople_set.all())
        result_dict['result_str'] = result_str

        return JsonResponse(result_dict)

    else:
        # fixme later
        return reverse('signin')