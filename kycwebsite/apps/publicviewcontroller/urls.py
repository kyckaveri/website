from django.urls import path
from . import views

app_name = "publicviewcontroller"
urlpatterns = [
    path(r"", views.home, name="home"),
    path(r"members", views.members, name="members"),
    path(r"members/<int:year>", views.members_by_year, name="members_by_year"),
    path(r"projects", views.projects, name="projects"),
]
