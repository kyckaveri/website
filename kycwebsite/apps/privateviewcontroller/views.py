from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login as django_login


def login(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('publicviewcontroller:home'))
        return HttpResponseRedirect(reverse('privateviewcontroller:admindashboard'))

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
        return HttpResponseRedirect(reverse('privateviewcontroller:admindashboard'))
    else:
        return HttpResponseRedirect(reverse('privateviewcontroller:loginerror'))


def admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    return render(request, 'privateviewcontroller/dashboard.html')
