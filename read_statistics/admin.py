from django.contrib import admin
from read_statistics.models import ReadNum,ReadDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['object_id','read_num','content_type','content_object']

@admin.register(ReadDetail)
class ReadDetailmAdmin(admin.ModelAdmin):
    list_display = ['object_id','date','read_num','content_type','content_object']