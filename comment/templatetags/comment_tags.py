from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from comment.form import CommentForm
register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.id).count()

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return CommentForm(initial={'content_type': content_type.model, 'object_id': obj.id, 'reply_comment_id': 0})

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.id, parent=None).order_by('-comment_time')
