from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login as django_login


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/admin')

    return render(request, 'privateviewcontroller/login.html')


def login_error(request):
    context = {
        "message": "Sorry wrong username/password"
    }
    return render(request, 'privateviewcontroller/login.html', context=context)


def login_handler(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return HttpResponseRedirect('/admin')
    else:
        return HttpResponseRedirect(reverse('privateviewcontroller:loginerror'))
