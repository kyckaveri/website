from django.shortcuts import render, HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage


def home(request):
    context = {
        "page_name": "home",
        "image_names": [staticfiles_storage.url("publicviewcontroller/img/home/home2.JPG"), staticfiles_storage.url("publicviewcontroller/img/home/home3.JPG")],
        "image_iterable": range(2, 4),
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
