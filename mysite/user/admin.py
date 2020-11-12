from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_no', 'is_active', 'user_id', 'user_name', 'user_birth', 'user_spicy', 'country_no',]
    list_display_links = ['user_id',]
    list_filter = ['is_active', 'user_spicy', 'country_no',]


class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_no', 'country_ko_name', 'country_en_name',]
    list_display_links = ['country_ko_name',]


class MapUserFoodClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_no', 'food_class_no',]
    list_display_links = ['id',]


class MapUserAllergyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_no', 'allergy_no',]
    list_display_links = ['id',]


class MapUserEatAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_no', 'food_no', 'is_written']
    list_display_links = ['id',]


admin.site.register(User, UserAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(MapUserFoodClass, MapUserFoodClassAdmin)
admin.site.register(MapUserAllergy, MapUserAllergyAdmin)
admin.site.register(MapUserEat, MapUserEatAdmin)
