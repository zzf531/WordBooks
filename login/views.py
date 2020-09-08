import os
import json
import hashlib
from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm, RegisterForm
from CONFIG import *


def login(request):
    """
    登录视图,判断是否已经登录,判断请求,验证form,和数据库进行比对.
    * 操作session
    request.session['is_login']
    request.session['user_id']
    request.session['user_name']
    request.session['word_path']
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    path = PATH + user.name + '.json'
                    request.session['word_path'] = path
                    return redirect('/get_keyword')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def index(request):
    """
    动态页视图,判断是否登录,获取所有用户,今日时间与用户单词本time字段进行比较,
    得到{用户名: 用户今日新增单词数量} 的dist   循环存入list
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        # user_list = User.objects.filter().exclude(name=request.session.get('user_name'))
        user_list = User.objects.all()
        user_new_add_word = []  # 用户今日新增单词
        for name in user_list:
            path = PATH + str(name) + '.json'
            if os.path.exists(path):  # 如果有这个单词本.进入这个单词本匹配时间
                num = [json.loads(line) for line in open(path) if json.loads(line).get('date')[:10] == Today_Time]
                amount = len(num)
                if amount:  # 去掉新增为0
                    user_new_add_word.append({'user': str(name), 'amount': amount})
        context = {
            'user_list': user_list,
            'user_new_add_word': user_new_add_word
        }
        return render(request, 'login/index.html', context)
    return render(request, 'login/index.html')


def register(request):
    """
    注册视图,判断是否已经登录,判断请求,验证form,注册表单存库
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    """
    删除所有session logout
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
