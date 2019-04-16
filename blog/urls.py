"""BlogProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
urlpatterns = [
    path('',views.blog_list,name="blog_list"),
    path('<int:blog_id>',views.blog_detail,name="blog_detail"),
    path('type/<int:blog_type_pk>',views.blog_with_type,name="blog_with_type"),
    path('date/<int:year>/<int:month>',views.blog_with_date,name="blog_with_date"),

]
