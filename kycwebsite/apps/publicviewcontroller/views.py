from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import KYCMember, Project, KYCYearSnapshot, CarouselImage, KYCJuniorMember, JuniorPosition
from .utils import get_project_obj, get_context

from datetime import datetime


def home(request):
    members_list = [member for member in KYCMember.objects.all().filter(deleted=False) if
                    member.position.importance is not 100]
    members_list.sort()
    member_list = [(member.position.position_name, member.name) for member in members_list]

    junior_members_list = [member for member in KYCJuniorMember.objects.all().filter(deleted=False) if
                           member.position.importance is not 100]
    junior_members_list.sort()
    junior_members_list = [(member.position.position_name, member.name) for member in junior_members_list]

    projects_list = [project for project in Project.objects.all().filter(deleted=False).order_by('-date') if
                     project.display]
    hours = int(sum([project.hours * project.members_attended for project in
                     [project for project in Project.objects.all().filter(deleted=False)]]))

    images = [image.image_url for image in CarouselImage.objects.all().filter(deleted=False).order_by('index')]

    context = get_context(request, 'home')

    context["first_image"] = images[0] if len(images) > 0 else ""
    context["images"] = images

    context["member_summary"] = member_list[:3] if len(member_list) > 3 else member_list
    context["member_expand"] = member_list[3:] if len(member_list) > 3 else None

    if context["member_expand"] is None:
        context["member_expand"] = junior_members_list if len(junior_members_list) > 0 else None
    else:
        context["member_expand"].extend(junior_members_list)

    context["has_expansion"] = len(context["member_expand"]) > 0 if context["member_expand"] is not None else False

    context["hours"] = hours if hours > 0 else 1

    try:
        context["projects"] = [get_project_obj(projects_list[i]) for i in range(4)]  # get only the first four projects,
        context["columns"] = [[get_project_obj(projects_list[i]) for i in range(0, 2)],
                              [get_project_obj(projects_list[i]) for i in
                               range(2, 4)]]  # get only the first four projects
    except IndexError:
        context["projects"] = []
        context["columns"] = []

    return render(request, 'publicviewcontroller/home.html', context=context)


def members(request):
    return HttpResponseRedirect(reverse('publicviewcontroller:members_by_year', kwargs={'year': datetime.now().year}))


def members_by_year(request, year):
    snapshots = KYCYearSnapshot.objects.order_by('-year')
    years = [datetime.now().year]
    extension = [snapshot.year for snapshot in snapshots]
    if datetime.now().year in extension:
        years = extension
    else:
        years.extend(extension)

    try:
        snapshotobj = snapshots.get(year=year)
        snapshot = snapshotobj.get()
        junior_snapshot = snapshotobj.get_junior()
    except KYCYearSnapshot.DoesNotExist:
        if year == datetime.now().year:
            snapshotobj = KYCYearSnapshot()
            snapshotobj.set()
            snapshot = snapshotobj.get()
            junior_snapshot = snapshotobj.get_junior()
        else:
            return HttpResponseRedirect(reverse('publicviewcontroller:members'))

    context = get_context(request, "members")
    context["snapshot"] = snapshot
    context["juniorsnapshot"] = junior_snapshot
    context["years"] = years
    context["year"] = year

    return render(request, 'publicviewcontroller/members.html', context=context)


def projects(request):
    column_one = []
    column_two = []
    column_three = []
    all_projects = []

    for index, project in enumerate(
            [p for p in Project.objects.all().filter(deleted=False).order_by('-date') if p.display]):
        project_obj = get_project_obj(project)
        all_projects.append(project_obj)
        if index % 3 == 0:
            column_one.append(project_obj)
        elif index % 3 == 1:
            column_two.append(project_obj)
        elif index % 3 == 2:
            column_three.append(project_obj)

    context = get_context(request, 'projects')
    context["columns"] = [column_one, column_two, column_three]
    context["all_projects"] = all_projects
    return render(request, 'publicviewcontroller/projects.html', context=context)
