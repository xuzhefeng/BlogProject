from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
# from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail
class BlogType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '博客分类表'

    def __str__(self):
        return self.name

class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=32)
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    '''
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
     '''
    class Meta:
        verbose_name_plural = "博客表"
        ordering = ['-created_time']

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_id':self.id})
    def get_email(self):
        return self.author.email
    def get_user(self):
        return self.author
    def __str__(self):
        return "<Blog:%s>" % self.title

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
'''
