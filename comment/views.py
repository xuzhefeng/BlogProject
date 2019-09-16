from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.form import CommentForm
from django.http import JsonResponse

def update_comment(request):
    data = {}
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent:
            comment.root = parent.root if parent.root else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()



        #评论/回复成功,返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        data['reply_to'] = comment.reply_to.get_nickname_or_username() if parent else None
        data['id'] = comment.id
        data['root_id'] = comment.root.id if parent else None
        data['content_type'] = ContentType.objects.get_for_model(comment).model



    # 评论/回复失败
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)

