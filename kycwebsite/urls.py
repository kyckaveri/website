"""KYC Website URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^', include('kycwebsite.apps.publicviewcontroller.urls')),
    url(r'^', include('kycwebsite.apps.privateviewcontroller.urls')),
]
