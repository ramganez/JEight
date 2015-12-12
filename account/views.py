from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


from account.forms import SigninForm

# Create your views here.


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
                    return redirect('roomexpenses:home')
            else:
                form = SigninForm()
    else:
        form = SigninForm()
    return render(request, 'account/signin.html', {'signin_form': form})
