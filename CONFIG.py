import time
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

PATH = "englishs/"
case_PATH = "englishs/case/"

# PATH = "/home/ubuntu/Wordbook/englishs/"
# case_PATH = "/home/ubuntu/Wordbook/englishs/case/"


def paginator(request, path, objects):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    objects = objects
    number = len(objects)
    for i in objects:
        i['num'] = number
        number -= 1
    p = Paginator(objects, 30, request=request)
    p = Paginator(objects, 20, request=request)
    records = p.page(page)
    return records


Today_Time = time.strftime("%Y-%m-%d", time.localtime())
__versions = '测试提交'

