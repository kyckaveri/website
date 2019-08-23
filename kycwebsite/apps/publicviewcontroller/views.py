from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage

from .models import KYCMember, Project, KYCYearSnapshot

from functools import reduce
from datetime import datetime


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
    return HttpResponseRedirect(reverse('publicviewcontroller:members_by_year', kwargs={'year': datetime.now().year}))


def members_by_year(request, year):
    login_name = 'Login'
    if request.user.is_authenticated:
        login_name = request.user

    snapshots = KYCYearSnapshot.objects.order_by('-year')
    years = [snapshot.year for snapshot in snapshots]

    try:
        snapshot = snapshots.get(year=year).get()
    except KYCYearSnapshot.DoesNotExist:
        return HttpResponseRedirect(reverse('publicviewcontroller:members'))

    context = {
        "page_name": "members",
        "snapshot": snapshot,
        "years": years,
        "year": year,
        "login_name": login_name
    }

    return render(request, 'publicviewcontroller/members.html', context=context)


def projects(request):
    login_name = 'Login'
    if request.user.is_authenticated:
        login_name = request.user

    column_one = []
    column_two = []
    column_three = []
    all_projects = []

    for index, project in enumerate([p for p in Project.objects.all().order_by('-date') if p.display]):
        project_obj = {
            "NAME": project.project_name,
            "IMAGE": project.image_url,
            "VOLUNTEERS": project.members_attended,
            "DATE": f"{project.date.month}/{project.date.day}/{str(project.date.year)[2:]}"
        }
        all_projects.append(project_obj)
        if index % 3 == 0:
            column_one.append(project_obj)
        elif index % 3 == 1:
            column_two.append(project_obj)
        elif index % 3 == 2:
            column_three.append(project_obj)

    context = {
        "page_name": "projects",
        "column_one": column_one,
        "column_two": column_two,
        "column_three": column_three,
        "all_projects": all_projects,
        "login_name": login_name,
    }
    return render(request, 'publicviewcontroller/projects.html', context=context)
