from read_statistics.models import ReadNum, ReadDetail
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
import datetime

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)

    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        #文章阅读数加一
        readnum, created = ReadNum.objects.get_or_create(object_id=obj.id, content_type=ct)
        # 计数加1
        readnum.read_num += 1
        readnum.save()

        #当天总阅读数加一
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(object_id=obj.id, content_type=ct, date=date)
        # 计数加1
        readDetail.read_num += 1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime("%m/%d"))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums

#获取今天的热门微博
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]
#获取昨天的热门微博
def get_yesterday_hot_data(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]
#获取七天内的热门微博
def get_7days_hot_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    # read_details = ReadDetail.objects.filter(content_type=content_type, date__lte=today, date__gt=date).annotate(read_num_sum=Sum('read_num')).order_by('-read_num')
    blogs = Blog.objects.filter(read_details__date__lte=today, read_details__date__gt=date)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:7]