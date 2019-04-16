from django.shortcuts import render,HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from blog.models import Blog,BlogType
from user.form import LoginForm
from read_statistics.utils import read_statistics_once_read

# Create your views here.
def get_blog_list_common_data(request,blog_list_all):
    current_page = request.GET.get('page')  # 获取当前页码
    paginator = Paginator(blog_list_all, settings.EACH_PAGE_BLOGS_NUMBER)
    page_of_blogs = paginator.get_page(current_page)  # 页码是非数字,则返回第一页
    current_page = page_of_blogs.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(current_page - 2, 1), current_page)) + \
                 list(range(current_page, min(current_page + 2, paginator.num_pages) + 1))
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    content = {}
    content["page_range"] = page_range
    content["page_of_blogs"] = page_of_blogs
    content['blogs'] = page_of_blogs.object_list
    content['blog_types'] = BlogType.objects.annotate(blog_count=Count("blog"))
    content['blog_dates'] = blog_dates_dict
    return content

def blog_list(request):
    blog_list_all = Blog.objects.all()
    content = get_blog_list_common_data(request,blog_list_all)
    return render(request,"blog/blog_list.html",content)

def blog_detail(request,blog_id):
    blog = Blog.objects.filter(id=blog_id).first()
    # blog = Blog.objects.get(id=blog_id)
    blog_content_type = ContentType.objects.get_for_model(blog)
    print('blog_detail-->',blog_content_type,type(blog_content_type))
    read_cookie_key = read_statistics_once_read(request, blog)

    content = {}
    content['blog'] = blog
    content['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    content['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    content['read_num'] = blog.get_read_num()
    content['login_form'] =LoginForm()
    response = render(request,'blog/blog_detail.html',content)
    response.set_cookie(read_cookie_key, 'true') #阅读cookies标记
    return response

def blog_with_type(request,blog_type_pk):
    blog_list_all = Blog.objects.filter(blog_type_id=blog_type_pk)
    content = get_blog_list_common_data(request,blog_list_all)
    content['blog_type'] = BlogType.objects.filter(id=blog_type_pk).first()
    return render(request, "blog/blog_with_type.html", content)

def blog_with_date(request,year,month):
    blog_list_all = Blog.objects.filter(created_time__year=year, created_time__month=month)
    content = get_blog_list_common_data(request, blog_list_all)
    content['blog_date'] = "%s年%s月" % (year, month)
    return render(request, "blog/blog_with_date.html", content)

