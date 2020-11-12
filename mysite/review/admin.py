from django.contrib import admin

from .models import *


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_no', 'food_no', 'rev_date', 'rev_star', 'rev_spicy', 'rev_contents']
    list_display_links = ['food_no',]
    list_filter = ['user_no', 'food_no', 'rev_star', 'rev_spicy']


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag_no', 'tag_ko_name', 'tag_en_name']
    list_display_links = ['tag_ko_name',]


class MapFoodTagAdmin(admin.ModelAdmin):
    list_display = ['rev_no', 'food_no', 'tag_no']
    list_display_links = ['rev_no',]


class MapUserTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_no', 'tag_no']
    list_display_links = ['id',]


admin.site.register(Review, ReviewAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(MapFoodTag, MapFoodTagAdmin)
admin.site.register(MapUserTag, MapUserTagAdmin)
