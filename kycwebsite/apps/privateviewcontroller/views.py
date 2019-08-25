from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from ..publicviewcontroller.models import Position, KYCMember


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

    context = {
        "positions": [position.position_name for position in Position.objects.all().order_by('importance')],
        "members": [{"INDEX": index, "MEMBER_NAME": member.name} for index, member in enumerate(members)],
        "message": message,
    }

    return render(request, 'privateviewcontroller/dashboard.html', context=context)


def add_member(request):
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


def remove_member(request, index):
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
        "positions": [position.position_name for position in Position.objects.all().order_by('importance')]
    }
    return render(request, 'privateviewcontroller/editmember.html', context=context)
