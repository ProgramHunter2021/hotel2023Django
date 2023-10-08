from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('at_id', 'at_name')

@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('a_name', 'a_date')