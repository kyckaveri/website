from django.shortcuts import render, HttpResponse


def home(request):
    return render(request, 'publicviewcontroller/home.html')
