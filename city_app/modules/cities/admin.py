from django.contrib import admin

from modules.cities.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'location')
