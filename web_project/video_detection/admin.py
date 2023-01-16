from django.contrib import admin
from .models import Video_feed

# Register your models here.


class video_feed_admin(admin.ModelAdmin):
    list_display = ('id', 'description', 'path', 'uploaded_at')


admin.site.register(Video_feed, video_feed_admin)
