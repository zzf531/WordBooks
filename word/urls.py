from django.conf.urls import url, include
from django.urls import path
from . import views, word_view
from login import views as lv
from django.views.generic.base import RedirectView

app_name = 'english'
urlpatterns = [
    path('', views.index, name='index'),
    path('2', views.i2, name='i2'),
    path('get_keyword', views.get_keyword, name='get_keyword'),
    url(r'^show_word$', views.show_word, name='show_word'),
    url(r'^del_word/(?P<pk>([^\u4e00-\u9fa5])*)/$', views.del_word, name='del_word'),
    url(r'^del_word/(?P<pk>(\w)*)/$', views.del_word, name='del_word'),
    url(r'^write_word/(?P<pk>(\w)*)/$', views.write_word, name='write_word'),
    url(r'^write_word/(?P<pk>([^\u4e00-\u9fa5])*)/$', views.write_word, name='write_word'),
    url(r'^add_word/(?P<pk>(\w)*)/$', views.add_word, name='add_word'),
    url(r'^add_word/(?P<pk>([^\u4e00-\u9fa5])*)/$', views.add_word, name='add_word'),

    url(r'^example/', word_view.example),  # 广场页
    url(r'^show_user_word/(?P<pk>([^\u4e00-\u9fa5])*)/$', word_view.show_user_word, name='show_user_word'),  # 显示用户单词本
    url(r'^show_case_word/(?P<pk>([^\u4e00-\u9fa5])*)$', word_view.show_case_word, name='show_case_word'),  # 显示标准单词本
    url(r'^xiaoxue/', word_view.xiaoxue, name='xiaoxue'),  # 小学
    url(r'^chuzhong/', word_view.chuzhong, name='chuzhong'),
    url(r'^gaozhong/', word_view.gaozhong, name='gaozhong'),
]
