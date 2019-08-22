from django.shortcuts import render, HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from .models import KYCMember, Project

from functools import reduce


def home(request):
    members_list = [member for member in KYCMember.objects.all() if member.position.importance < 5]
    members_list.sort()
    member_list = [(member.position.position_name, member.name) for member in members_list]

    projects_list = [project for project in Project.objects.all() if project.display]
    projects_list.sort()
    hours = reduce(lambda x, y: x + y, [project.hours * project.members_attended for project in projects_list])

    login_name = 'Login'
    if request.user.is_authenticated:
        login_name = request.user

    context = {
        "page_name": "home",
        "images": [staticfiles_storage.url(f"publicviewcontroller/img/home/home{x + 1}.JPG") for x in range(2)],
        "first_image": staticfiles_storage.url("publicviewcontroller/img/home/home1.JPG"),
        "has_expansion": len(member_list) > 3,
        "member_summary": member_list[:3] if len(member_list) > 3 else member_list,
        "member_expand": member_list[3:] if len(member_list) > 3 else None,
        "hours": hours,
        "project_info": [(projects_list[i].project_name, projects_list[i].date, projects_list[i].image_url) for i in
                         range(3)],  # get only the first three projects,
        "login_name": login_name
    }
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
