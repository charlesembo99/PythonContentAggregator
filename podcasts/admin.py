from django.contrib import admin

# Register your models here.
from .models import Episode

@admin.register(Episode)

class AdminEpisode(admin.ModelAdmin):
    list_display = ['postcast_name','title','thumbnail']

