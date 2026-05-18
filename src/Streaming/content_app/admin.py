from content_app import models
from django.contrib import admin

admin.site.register(models.Content)
admin.site.register(models.Comment)