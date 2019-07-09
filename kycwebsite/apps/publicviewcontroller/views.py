from django.shortcuts import render, HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage


def home(request):
    context = {
        "page_name": "home",
        "images": [staticfiles_storage.url(f"publicviewcontroller/img/home/home{x + 1}.JPG") for x in range(2)],
        "first_image": staticfiles_storage.url("publicviewcontroller/img/home/home1.JPG"),
    }
    print(context["images"])
    return render(request, 'publicviewcontroller/home.html', context=context)


def members(request):
    context = {
        "page_name": "members",
    }
    return render(request, 'publicviewcontroller/members.html', context=context)


def projects(request):
    context = {
        "page_name": "projects",
    }
    return render(request, 'publicviewcontroller/projects.html', context=context)
