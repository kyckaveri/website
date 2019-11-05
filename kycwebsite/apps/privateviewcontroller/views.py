from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from dateutil.parser import parse

from ..publicviewcontroller.models import Position, JuniorPosition, KYCMember, KYCJuniorMember, Project, \
    KYCYearSnapshot, CarouselImage

from datetime import datetime


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


def logout_handler(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('privateviewcontroller:login'))


def admin_dashboard(request, message=None):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    members = [m for m in KYCMember.objects.all().filter(deleted=False)]
    members.sort()
    junior_members = [m for m in KYCJuniorMember.objects.all().filter(deleted=False)]
    junior_members.sort()

    projects = [p for p in Project.objects.all().filter(deleted=False)]
    projects.sort(reverse=True)

    images = [{
        "name": i.name,
        "image_url": i.image_url,
        "index": i.index
    } for i in CarouselImage.objects.all().filter(deleted=False).order_by('index')]

    context = {
        "positions": [position.position_name for position in Position.objects.all().order_by('importance')],
        "junior_positions": [position.position_name for position in
                             JuniorPosition.objects.all().order_by('importance')],
        "members": [{"INDEX": index, "MEMBER_NAME": member.name} for index, member in enumerate(members)],
        "junior_members": [{"INDEX": index, "MEMBER_NAME": member.name} for index, member in enumerate(junior_members)],
        "projects": [{
            "INDEX": index,
            "NAME": project.project_name,
            "DATE": f"{project.date.month}/{project.date.day}/{project.date.year}"
        } for index, project in enumerate(projects)],
        "images": images,
        "message": message,
    }

    return render(request, 'privateviewcontroller/dashboard.html', context=context)


def add_member(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    try:
        name = request.POST["name"]
        position_name = request.POST["position"]
    except KeyError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error creating new member"}))

    position = Position.objects.filter(position_name=position_name).first()
    new_member = KYCMember(name=name, position=position)
    new_member.save()

    return HttpResponseRedirect(
        reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Created new member: {name}"}))


def add_junior_member(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    try:
        name = request.POST["name"]
        position_name = request.POST["position"]
    except KeyError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error creating new member"}))
    position = JuniorPosition.objects.filter(position_name=position_name).first()
    new_member = KYCJuniorMember(name=name, position=position)
    new_member.save()

    return HttpResponseRedirect(
        reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Created new junior member: {name}"}))


def remove_member(request, index):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    try:
        members = [m for m in KYCMember.objects.all().filter(deleted=False)]
        members.sort()
        member = members[index]
    except IndexError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error removing member"}))

    member.deleted = True
    member.save()
    return HttpResponseRedirect(
        reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Removed member: {member.name}"}))


def edit_member(request, index=None):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    if index is None:
        try:
            name = request.POST["name"]
            original = request.POST["original_name"]
            position_name = request.POST["member_position"]
        except KeyError:
            return HttpResponseRedirect(
                reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error editing member"}))

        member = KYCMember.objects.all().filter(deleted=False).filter(name=original).first()
        position = Position.objects.all().filter(position_name=position_name).first()

        try:
            member.name = name
            member.position = position
            member.save()
        except:
            return HttpResponseRedirect(
                reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error editing member"}))

        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Edited member: {member.name}"}))

    try:
        members = [m for m in KYCMember.objects.all().filter(deleted=False)]
        members.sort()
        member = members[index]
    except IndexError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error editing member"}))

    context = {
        "member": {
            "name": member.name,
            "position": member.position.position_name
        },
        "positions": [position.position_name for position in Position.objects.all().order_by('importance')],
        "index": index
    }
    return render(request, 'privateviewcontroller/editmember.html', context=context)


def add_project(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    try:
        project_name = request.POST["project_name"]
        hours = float(request.POST["hours"])
        members_attended = int(float(request.POST["members_attended"]))
        date = request.POST["date"]
        image_url = request.POST["image_url"]
    except KeyError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error creating new project"}))
    except ValueError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error creating new project"}))

    date = parse(date)

    try:
        display = request.POST["display"]
    except KeyError:
        display = 'off'

    display = display == 'on'

    new_project = Project(project_name=project_name, display=display, hours=hours, members_attended=members_attended,
                          date=date, image_url=image_url)
    new_project.save()

    return HttpResponseRedirect(
        reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Created new project: {project_name}"}))


def edit_project(request, index=None):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    if index is None:
        try:
            project_name = request.POST["project_name"]
            hours = float(request.POST["hours"])
            members_attended = int(float(request.POST["members_attended"]))
            date = request.POST["date"]
            image_url = request.POST["image_url"]
            original = request.POST["original"]
        except KeyError:
            return HttpResponseRedirect(
                reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error editing project"}))
        except ValueError:
            return HttpResponseRedirect(
                reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error editing project"}))

        date = parse(date)

        try:
            display = request.POST["display"]
        except KeyError:
            display = 'off'

        display = display == 'on'
        project = Project.objects.all().filter(deleted=False).filter(image_url=original).first()

        try:
            project.project_name = project_name
            project.display = display
            project.hours = hours
            project.members_attended = members_attended
            project.date = date
            project.image_url = image_url
            project.save()
        except:
            return HttpResponseRedirect(
                reverse('privateviewcontroller:admindashboard',
                        kwargs={"message": "Error editing project (211 Error)"}))

        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Edited project: {project_name}"}))

    try:
        projects = [p for p in Project.objects.all().filter(deleted=False)]
        projects.sort(reverse=True)
        project = projects[index]
    except IndexError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error editing member"}))

    context = {
        "project": {
            "project_name": project.project_name,
            "display": project.display,
            "hours": project.hours,
            "members_attended": project.members_attended,
            "date": f"{project.date.year}-{project.date.month if project.date.month > 9 else f'0{project.date.month}'}-{project.date.day if project.date.day > 9 else f'0{project.date.day}'}",
            "image_url": project.image_url,
        },
        "index": index
    }
    return render(request, 'privateviewcontroller/editproject.html', context=context)


def remove_project(request, index):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    try:
        projects = [p for p in Project.objects.all().filter(deleted=False)]
        projects.sort(reverse=True)
        project = projects[index]
    except IndexError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error removing project"}))

    project.deleted = True
    project.save()
    return HttpResponseRedirect(
        reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Removed project: {project.project_name}"}))


def create_snapshot(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    snapshot = KYCYearSnapshot(year=datetime.now().year)
    snapshot.set()
    snapshot.save()

    for member in KYCMember.objects.all().filter(deleted=False):
        member.deleted = True
        member.save()

    return HttpResponseRedirect(
        reverse('privateviewcontroller:admindashboard',
                kwargs={"message": f"Created snapshot, please add all new members"}))


def add_image(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    try:
        name = request.POST["name"]
        image_url = request.POST["image_url"]
    except KeyError:
        return HttpResponseRedirect(
            reverse('privateviewcontroller:admindashboard', kwargs={"message": "Error adding new image"}))

    try:
        index = CarouselImage.objects.all().filter(deleted=False).order_by('index').last().index
    except:
        index = -1
    index += 1

    new_image = CarouselImage(name=name, image_url=image_url, index=index)
    new_image.save()

    return HttpResponseRedirect(
        reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Added new image: {name}"}))


def remove_image(request, index):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('publicviewcontroller:home'))

    image = CarouselImage.objects.all().filter(deleted=False).filter(index=index).first()
    image.deleted = True
    image.save()

    return HttpResponseRedirect(
        reverse('privateviewcontroller:admindashboard', kwargs={"message": f"Removed image: {image.name}"}))
