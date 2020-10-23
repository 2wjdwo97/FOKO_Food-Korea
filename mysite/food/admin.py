from django.contrib import admin

from .models import *


class FoodClassAdmin(admin.ModelAdmin):
    list_display = ['food_class_no', 'food_class_ko_name', 'food_class_en_name']
    list_display_links = ['food_class_ko_name']

    class Meta:
        verbose_name = "FoodClass"
        verbose_name_plural = "FoodClasses"


class AllergyClassAdmin(admin.ModelAdmin):
    list_display = ['allergy_no', 'allergy_ko_name', 'allergy_en_name']
    list_display_links = ['allergy_ko_name']

    class Meta:
        verbose_name = "AllergyClass"
        verbose_name_plural = "AllergyClasses"


class FoodAdmin(admin.ModelAdmin):
    list_display = ['food_no', 'food_name', 'food_dsc', 'food_class_no']
    list_display_links = ['food_no']
    list_editable = ['food_name', 'food_dsc']
    list_filter = ['food_class_no']

    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Foods"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['ingre_no', 'ingre_ko_name', 'ingre_en_name', 'allergy_no']
    list_display_links = ['ingre_no']
    list_editable = ['ingre_ko_name', 'ingre_en_name']
    list_filter = ['allergy_no']

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"


admin.site.register(FoodClass, FoodClassAdmin)
admin.site.register(AllergyClass, AllergyClassAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Ingredient, IngredientAdmin)
