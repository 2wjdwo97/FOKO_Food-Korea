from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_no', 'is_active', 'user_id', 'user_name', 'user_birth', 'user_spicy', 'country_no',]
    list_display_links = ['user_id',]
    list_filter = ['user_spicy', 'country_no',]


class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_no', 'country_ko_name', 'country_en_name',]
    list_display_links = ['country_ko_name',]


admin.site.register(User, UserAdmin)
admin.site.register(Country, CountryAdmin)
