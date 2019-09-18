from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
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
        # 不存在，则获取数据，并写入缓存
        hot_data_for_7_days = get_7days_hot_data()
        # 写入缓存
        cache.set('hot_data_for_7_days', hot_data_for_7_days, 3600)
    content = {}
    content['dates'] = dates
    content['read_nums'] = read_nums
    content['today_hot_data'] = today_hot_data
    content['yesterday_hot_data'] = yesterday_hot_data
    content['hot_data_for_7_days'] = hot_data_for_7_days

    return render(request,"home.html",content)

def search(request):
    search_words = request.GET.get('wd', '').strip()
    #分词:按空格 & | ~
    condition = None
    if search_words != '':
        for search_word in search_words.split(' '):
            if not condition:
                condition = Q(title__icontains=search_word)
            else:
                condition = condition | Q(title__icontains=search_word)

    #搜索
    blogs = Blog.objects.none()
    if condition:
        blogs = Blog.objects.filter(condition)

    #分页
    current_page = request.GET.get('page', 1)  # 获取当前页码
    paginator = Paginator(blogs, 10)
    page_of_blogs = paginator.get_page(current_page)  # 页码是非数字,则返回第一页
    content = {}
    content['page_of_blogs'] = page_of_blogs
    content['search_words'] = search_words
    content['search_blogs_count'] = blogs.count()
    return render(request,'search.html', content)
