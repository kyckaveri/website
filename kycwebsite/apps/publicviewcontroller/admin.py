from django.contrib import admin
from .models import Position, KYCMember, Project, KYCYearSnapshot

admin.site.register(Position)
admin.site.register(KYCMember)
admin.site.register(Project)
admin.site.register(KYCYearSnapshot)
