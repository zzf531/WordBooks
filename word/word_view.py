import os
import json
import hashlib
from django.shortcuts import render, redirect
from login.models import User
from CONFIG import *


def example(request):
    return render(request, 'example/home_page2.html')


def xiaoxue(request):
    return render(request, 'example/Primary_School.html')


def chuzhong(request):
    return render(request, 'example/chuzhong.html')


def gaozhong(request):
    return render(request, 'example/gaozhong.html')


def show_case_word(request, pk):
    """
    查看案例单词本视图,path为路径+pk
    :param request:
    :param pk: 前段url传入 -> string
    :return:
    """
    path = case_PATH + pk + '.json'
    objects = [json.loads(line) for line in open(path)]
    records = paginator(request, path, objects)
    context = {
        'records': records,
        'add': 1
    }
    return render(request, '_show.html', context)


def show_user_word(request, pk):
    """
    动态页学习大家单词本, 判断对方单词本是否写入,为空创建session,如果点击另一个用户单词本,存在判断以前
    是否生成了session,将他删除, 否则session会一直存在,
    将单词本里的json数据,转换为dict,全部存入list
    :param request:
    :return: list放入一个字典,django不能返回list
    """
    path = PATH + pk + '.json'
    if not os.path.exists(path):
        request.session['message'] = '对方的单词本为空!'
        return redirect('/index')

    if request.session.get('message', None):
        del request.session['message']
    objects = [json.loads(line) for line in open(path)][::-1]
    records = paginator(request, path, objects)
    context = {
        'records': records,
        'add': 1
    }
    return render(request, '_show.html', context)
