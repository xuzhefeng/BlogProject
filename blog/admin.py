from django.contrib import admin
from blog import models

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id','title','blog_type','author','get_read_num','created_time','last_updated_time',]
# admin.site.register(models.Blog,BlogAdmin)

@admin.register(models.BlogType)
class BlogTypedmin(admin.ModelAdmin):
    list_display = ['id','name',]
'''
@admin.register(models.ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['blog','read_num']
    '''