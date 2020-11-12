from django.contrib import admin

from .models import *


class FoodClassAdmin(admin.ModelAdmin):
    list_display = ['food_class_no', 'food_class_ko_name', 'food_class_en_name']
    list_display_links = ['food_class_ko_name']


class AllergyClassAdmin(admin.ModelAdmin):
    list_display = ['allergy_no', 'allergy_ko_name', 'allergy_en_name']
    list_display_links = ['allergy_ko_name']


class FoodAdmin(admin.ModelAdmin):
    list_display = ['food_no', 'food_name', 'food_star', 'food_dsc', 'food_class_no']
    list_display_links = ['food_no']
    list_editable = ['food_name', 'food_dsc']
    list_filter = ['food_class_no']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['ingre_no', 'ingre_ko_name', 'ingre_en_name', 'allergy_no']
    list_display_links = ['ingre_no']
    list_filter = ['allergy_no']


class MapFoodIngreAdmin(admin.ModelAdmin):
    list_display = ['id', 'food_no', 'ingre_no']
    list_display_links = ['id']
    # list_editable = ['food_no', 'ingre_no']


class MapFoodIngreAddAdmin(admin.ModelAdmin):
    list_display = ['id', 'food_no', 'ingre_no']
    list_display_links = ['id']
    # list_editable = ['food_no', 'ingre_no']


admin.site.register(FoodClass, FoodClassAdmin)
admin.site.register(AllergyClass, AllergyClassAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MapFoodIngre, MapFoodIngreAdmin)
admin.site.register(MapFoodIngreAdd, MapFoodIngreAddAdmin)
