
from __future__ import unicode_literals
from .models import Student, Room, Diff, Swap, Change,Hostel, HostelImage
from django.contrib import admin
from django.contrib.auth.models import Group, User


class HostelImageInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = HostelImage
    extra = 1  # Number of empty forms to display

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'pricing', 'latitude', 'longitude')
    search_fields = ('name', 'address')
    inlines = [HostelImageInline]
    
admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Diff)
admin.site.register(Swap)
admin.site.register(Change)
# customization of Django Admin
admin.site.unregister(Group)
admin.site.site_header='Hostel Management Dashboard'
