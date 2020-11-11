from django.contrib import admin

from .models import *


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_no', 'food_no', 'rev_date', 'rev_star', 'rev_spicy', 'rev_contents']
    list_display_links = ['food_no',]
    list_filter = ['user_no', 'food_no', 'rev_star', 'rev_spicy']

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag_no', 'tag_ko_name', 'tag_en_name']
    list_display_links = ['tag_ko_name',]
    list_editable = ['tag_no', 'tag_en_name']

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


admin.site.register(Review, ReviewAdmin)
admin.site.register(Tag, TagAdmin)
