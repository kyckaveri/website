from django.shortcuts import render, HttpResponse


def home(request):
    context = {
        "page_name": "home",
    }
    return render(request, 'publicviewcontroller/home.html', context=context)


def members(request):
    context = {
        "page_name": "members",
    }
    return render(request, 'publicviewcontroller/home.html', context=context)


def projects(request):
    context = {
        "page_name": "projects",
    }
    return render(request, 'publicviewcontroller/home.html', context=context)
