from django.urls import path
from . import views

app_name = "privateviewcontroller"
urlpatterns = [
    path(r'login', views.login, name="login"),
    path(r'loginhandler', views.login_handler, name="loginhandler"),
    path(r'loginerror', views.login_error, name="loginerror"),
    path(r'logout', views.logout_handler, name="logout"),
    path(r'admin-dashboard/', views.admin_dashboard, name="admindashboard"),
    path(r'admin-dashboard/<str:message>/', views.admin_dashboard, name="admindashboard"),
    path(r'admin-dashboard/add/member/', views.add_member, name="addmember"),
    path(r'admin-dashboard/remove/member/<int:index>', views.remove_member, name="removemember"),
]
