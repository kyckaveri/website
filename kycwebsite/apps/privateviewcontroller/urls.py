from django.urls import path
from . import views

app_name = "privateviewcontroller"
urlpatterns = [
    path(r"login", views.login, name="login"),
    path(r"loginhandler", views.login_handler, name="loginhandler"),
    path(r"loginerror", views.login_error, name="loginerror"),
    path(r"logout", views.logout_handler, name="logout"),
    path(r"admin-dashboard/", views.admin_dashboard, name="admindashboard"),
    path(
        r"admin-dashboard/<str:message>/", views.admin_dashboard, name="admindashboard"
    ),
    path(r"admin-dashboard/add/member/", views.add_member, name="addmember"),
    path(
        r"admin-dashboard/add/juniormember/",
        views.add_junior_member,
        name="addjuniormember",
    ),
    path(
        r"admin-dashboard/remove/member/<int:index>",
        views.remove_member,
        name="removemember",
    ),
    path(r"admin-dashboard/edit/member/", views.edit_member, name="editmember"),
    path(
        r"admin-dashboard/edit/member/<int:index>", views.edit_member, name="editmember"
    ),
    path(r"admin-dashboard/add/project/", views.add_project, name="addproject"),
    path(r"admin-dashboard/edit/project/", views.edit_project, name="editproject"),
    path(
        r"admin-dashboard/edit/project/<int:index>",
        views.edit_project,
        name="editproject",
    ),
    path(
        r"admin-dashboard/remove/project/<int:index>",
        views.remove_project,
        name="removeproject",
    ),
    path(r"admin-dashboard/add/snapshot", views.create_snapshot, name="createsnapshot"),
    path(r"admin-dashboard/add/image", views.add_image, name="addimage"),
    path(
        r"admin-dashboard/remove/image/<int:index>",
        views.remove_image,
        name="removeimage",
    ),
]
