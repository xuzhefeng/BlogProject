from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data,get_7days_hot_data
from blog.models import Blog
# Create your views here.
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    # blog = Blog.objects.get(id=blog_id)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_data_for_7_days = cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days = get_7days_hot_data()
        cache.set('hot_data_for_7_days', hot_data_for_7_days, 3600)
    content = {}
    content['dates'] = dates
    content['read_nums'] = read_nums
    content['today_hot_data'] = today_hot_data
    content['yesterday_hot_data'] = yesterday_hot_data
    content['hot_data_for_7_days'] = hot_data_for_7_days
    return render(request,"home.html",content)

