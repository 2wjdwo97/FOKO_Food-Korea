from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_no', 'user_id', 'user_name', 'user_age', 'user_spicy', 'country_no')
    list_display_links = ('user_no',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_no', 'country_ko_name', 'country_en_name',)
    list_display_links = ('country_no',)
