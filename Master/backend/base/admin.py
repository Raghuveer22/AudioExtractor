from django.contrib import admin
from .models import Audio,Comment,Like
# Register your models here.
admin.site.register(Audio)
admin.site.register(Comment)  
admin.site.register(Like)