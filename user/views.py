from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
import random
import string
import time
from django.core.mail import send_mail
from .form import LoginForm,RegisterForm,ChangeNicknameForm,BindEmailForm,ChangePasswordForm,ForgotPasswordForm
from .models import Profile

def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('home')))

    else:
        login_form = LoginForm()
    content = {}
    content['login_form'] = login_form
    return render(request, 'user/login.html', content)
def login_for_modal(request):
    data = {}
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
        data['message'] = list(login_form.errors.values())[0][0]
    return JsonResponse(data)
def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST,request=request)

        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            #创建用户
            # user = User.objects.create_user(username, password, email)
            # user.save()
            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()
            #登录用户
            # user = auth.authenticate(username=username,password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('home')) )

    else:
        register_form = RegisterForm()
    content = {}
    content['register_form'] = register_form
    return render(request, 'user/register.html', content)
def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))
def user_info(request):
   return render(request, "user/user_info.html")
def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form= ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            new_nickname = form.cleaned_data['new_nickname']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = new_nickname
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    content = {}
    content['form'] = form
    content['page_title'] = '编辑个人信息'
    content['form_title'] = '设置昵称'
    content['submit_text'] = '提交'
    content['return_back_url'] = redirect_to
    return render(request, 'form.html', content)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form= BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    content = {}
    content['form'] = form
    content['page_title'] = '编辑个人信息'
    content['form_title'] = '绑定邮箱'
    content['submit_text'] = '绑定'
    content['return_back_url'] = redirect_to
    return render(request,'user/bind_email.html',content)
def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            request.user.set_password(new_password1)
            request.user.save()
            return redirect(reverse('login'))
    else:
        form = ChangePasswordForm()
    content = {}
    content['form'] = form
    content['page_title'] = '编辑个人信息'
    content['form_title'] = '修改密码'
    content['submit_text'] = '提交'
    content['return_back_url'] = redirect_to
    return render(request, 'form.html', content)
def forgot_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)


        if form.is_valid():
            email = form.cleaned_data['email']
            new_password1 = form.cleaned_data['new_password1']
            user = User.objects.get(email = email)
            user.set_password(new_password1)
            user.save()
            #清除session
            del request.session['forgot_password_code']
            return redirect(reverse('login'))
    else:
        form = ForgotPasswordForm()
    content = {}
    content['form'] = form
    content['page_title'] = '编辑个人信息'
    content['form_title'] = '重置密码'
    content['submit_text'] = '重置'
    content['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', content)

def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                '475308964@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
