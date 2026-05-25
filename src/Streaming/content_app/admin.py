from content_app import models
from django.contrib import admin

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'is_public')
    list_filter = ('content_type', 'is_public', 'status')
    search_fields = ('title',)


admin.site.register(models.Content, ContentAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Playlist)

