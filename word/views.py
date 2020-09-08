import os
import json
import fileinput
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .crawl import get_keywords
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from CONFIG import *
from django.http import HttpResponseRedirect


def i2(request):
    path = request.session['word_path']
    return render(request, 'a.html')


def index(request):
    return render(request, '_form.html', locals())


def get_keyword(request):
    """
    判断请求是否正确,获取表单要进行翻译的单词,返回单词的内容
    get_keywords方法调用有道词典接口进行查询,然后将返回的json进行格式化,保留需要的字段,返回字典
    result['test']测试字段,当翻译了单词时,才可以写入
    :param request:
    :return: 返回单词的汉,英,词条
    """
    result = {}
    if request.POST and request.POST['q']:
        i = get_keywords(request.POST['q'])
        try:
            result['test'] = 't'
            result['tgt'] = i.get('tgt')
            result['src'] = i.get('src')
            if i.get('entries'):
                result['entries'] = i.get('entries')
            content = {
                'result': result,
            }
            return render(request, '_form.html', content)
        except AttributeError:
            return render(request, '_form.html')
    return render(request, '_form.html')


def write_word(request, pk):
    """
    如果登录,获取被翻译的单词,将他追加存入单词本
    get_keywords方法调用有道词典接口进行查询,然后将返回的json进行格式化,保留需要的字段,返回字典
    转换为json格式,存入单词本
    request.session['word_path'] 为存储路径
    :param pk: 被翻译的单词
    :return: 重定向到/get_keyword
    """
    if not request.session.get('is_login', None):
        message = '没有登录,只能翻译.无法写入'
        context = {
            'message': message,
            't': 1,
        }
        return render(request, '_form.html', context)
    p = request.session['word_path']
    with open(p, 'a', encoding='utf-8') as file:
        file.write(json.dumps(get_keywords(pk), ensure_ascii=False) + '\n')
    return render(request, '_form.html', locals())


def show_word(request):
    """
    判断是否登录,和单词本是否写入,使用 Paginator 插件进行分页
    将单词本里的json数据,转换为dict,全部存入list
    :param request:
    :return: list放入一个字典,django不能返回list
    """
    if not request.session.get('is_login', None):
        message = '没有登录,没有单词本'
        context = {
            'message': message,
            't': 1,
        }
        return render(request, '_form.html', context)
    path = request.session['word_path']
    if not os.path.exists(path):
        message = '单词本为空,请先写入'
        return render(request, '_form.html', {'message': message})
    objects = [json.loads(link) for link in open(path)][::-1]
    records = paginator(request, path, objects)
    context = {
        'records': records,
        'delete': 1
    }
    return render(request, '_show.html', context)


def del_word(request, pk):
    """
    fileinput 一个库,删除被匹配的单词
    :param pk: 要删除的单词
    :param request:
    :return: 重定向
    """
    p = request.session['word_path']
    for line in fileinput.input(p, inplace=1):
        s = json.loads(line).get('src')
        if not s == pk:
            print(line.replace('\n', ''))
    return redirect('/show_word')


def add_word(request, pk):
    if not request.session.get('is_login', None):
        message = '没有登录,只能翻译.无法写入'
        context = {
            'message': message,
            't': 1,
        }
        return render(request, '_show.html', context)
    p = request.session['word_path']
    with open(p, 'a', encoding='utf-8') as file:
        file.write(json.dumps(get_keywords(pk), ensure_ascii=False) + '\n')
    print('=========================')
    print(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
