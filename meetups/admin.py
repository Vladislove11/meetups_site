from django.contrib import admin
from .models import Meetup, Location, Participant

# Register your models here.

@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "date", "location", "creator")
    list_filter = ("title", "date", "location", "creator",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address")

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("email",)