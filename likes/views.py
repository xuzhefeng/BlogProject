from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from .models import LikeRecord,LikeCount

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)
def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you are not login')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'object not exist')

    #点赞
    if request.GET.get('is_like') == 'true':
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        #未点赞过,进行点赞
        if created:
            #点赞数加1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        #已点赞过,不能重复点赞
        else:
            return ErrorResponse(402,'you were liked')
    #取消点赞
    else:
        #有点赞过,取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            like_record = LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                #总点赞数减1
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                #点赞数据异常
                return ErrorResponse(403,'data error')
        # 未点赞过,不能取消点赞
        else:
            return ErrorResponse(405,'you are not liked')

