from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from account.forms import SigninForm

# Create your views here.


class LoginRequiredMixin(object):

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


def signin(request):
    # ipdb.set_trace()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    return redirect('roomexpenses:month_expense')
            else:
                form = SigninForm()
    else:
        form = SigninForm()
    return render(request, 'account/signin.html', {'signin_form': form})


def signout(request):
    logout(request)
    return redirect('go-to-signin')