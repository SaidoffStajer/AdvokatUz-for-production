from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Constitution)
class ConstitutionAdmin(admin.ModelAdmin):
    list_display = ('file', 'link',)

@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_file', 'youtube_link',)

@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image',)
    readonly_fields = ('hit_count_generic',)

    def hit_count_generic(self, obj):
        # Display the actual hit count
        return obj.hit_count_generic.count() if obj.hit_count_generic else 0
    hit_count_generic.short_description = 'Hit Count'