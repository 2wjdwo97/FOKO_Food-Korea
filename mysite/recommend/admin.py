from django.contrib import admin

from .models import *


class FoodRankCountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'food_no', 'country_no', 'rank']
    list_display_links = ['id']


class FoodRankAgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'food_no', 'age', 'rank']
    list_display_links = ['id']


admin.site.register(FoodRankCountry, FoodRankCountryAdmin)
admin.site.register(FoodRankAge, FoodRankAgeAdmin)
