from django.contrib import admin

from forum.models import Comment, Thread

# Register your models here.

admin.site.register(Thread)
admin.site.register(Comment)
