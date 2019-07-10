from django.urls import path
from . import views

app_name = "privateviewcontroller"
urlpatterns = [
    path(r'login', views.login, name="login"),
    path(r'loginhandler', views.login_handler, name="loginhandler"),
    path(r'loginerror', views.login_error, name="loginerror")
]
