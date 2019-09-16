from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱',
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名或邮箱'}),
                               error_messages={'required':'用户名或邮箱不能为空'}
                               )
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}),
                               error_messages={'required': '密码不能为空'}
                               )

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError("用户名或者密码错误")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data
class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位的用户名'}))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入至少6位的密码'}))
    password2 = forms.CharField(label='再输入一次密码',
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'}))
    verification_code =forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}),
        error_messages={'required': '验证码不能为空'}
    )


    def __init__(self,*args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)
    def clean_username(self):
        username = self.cleaned_data['username']
        #判断用户名是否存在
        if User.objects.filter(username=username).exists():
            #用户名已经存在
            raise forms.ValidationError('用户名已经存在')
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('邮箱已被绑定')
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        # 判断密码是否一致
        if password != password2:
            raise forms.ValidationError('两次密码输入不一致')
        return password2
    def clean_verification_code(self):
        # 判断验证码
        code = self.request.session.get('register_code', '').lower()
        verification_code = self.cleaned_data.get('verification_code','').lower()
        if not (code != '' and  verification_code == code):
            raise forms.ValidationError('验证码不正确')
        return verification_code
class ChangeNicknameForm(forms.Form):
    new_nickname = forms.CharField(
        label='昵称',
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入昵称'}),
        error_messages={'required': '昵称不能为空'}
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm,self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    # def clean_new_nickname(self):
    #     new_nickname = self.cleaned_data.get('new_nickname', '').strip()
    #     if new_nickname == '':
    #         raise forms.ValidationError('新的昵称不能为空')
    #     return new_nickname

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
        error_messages={'required': '邮箱不能为空'}
    )
    verification_code =forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}),
        error_messages={'required': '验证码不能为空'}
    )
    def __init__(self,*args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        #判断用户是否已绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('用户已绑定邮箱')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('邮箱已被绑定')
        return email
    def clean_verification_code(self):
        # 判断验证码
        code = self.request.session.get('bind_email_code', '').lower()
        verification_code = self.cleaned_data.get('verification_code','').lower()
        if not (code != '' and  verification_code == code):
            raise forms.ValidationError('验证码不正确')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧的密码',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入旧的密码'}),
                                    error_messages={'required': '密码不能为空'}
                                    )
    new_password1 = forms.CharField(label='密码',
                                    min_length=6,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入至少6位的密码'}),
                                    error_messages={'required': '密码不能为空'}
                                    )
    new_password2 = forms.CharField(label='再输入一次密码',
                                    min_length=6,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再输入一次密码'}),
                                    error_messages={'required': '密码不能为空'}
                                    )
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm,self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if not self.user.is_authenticated:
            raise forms.ValidationError('用户未登录')

        #判断旧密码是否正确
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码不正确')

        return self.cleaned_data

    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        # 判断密码是否一致
        if new_password1 != new_password2 or new_password1 == '':
            raise forms.ValidationError('两次密码输入不一致')
        return new_password2

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入绑定过的邮箱'}))
    new_password1 = forms.CharField(label='新的密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入至少6位的新密码'}))
    new_password2 = forms.CharField(label='再输入一次密码',
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'}))
    verification_code =forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}),
        error_messages={'required': '验证码不能为空'}
    )


    def __init__(self,*args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email = email).exists():
            raise forms.ValidationError('邮箱未被绑定')
        return email

    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        # 判断密码是否一致
        if new_password1 != new_password2:
            raise forms.ValidationError('两次密码输入不一致')
        return new_password2

    def clean_verification_code(self):
        # 判断验证码
        code = self.request.session.get('forgot_password_code', '').lower()
        verification_code = self.cleaned_data.get('verification_code', '').lower()
        if not (code != '' and verification_code == code):
            raise forms.ValidationError('验证码不正确')
        return verification_code


