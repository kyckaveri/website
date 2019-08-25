from django.contrib import admin
from .models import KYCMember, Project, CarouselImage, Position, KYCYearSnapshot

admin.site.register(KYCMember)
admin.site.register(Project)
admin.site.register(CarouselImage)
admin.site.register(Position)
admin.site.register(KYCYearSnapshot)
