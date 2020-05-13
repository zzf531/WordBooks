from django.conf.urls import url
from django.contrib import admin
from login import views

app_name = 'login'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),  # 动态页
    url(r'^login/', views.login),  # 登录页
    url(r'^register/', views.register),  # 注册页
    url(r'^logout/', views.logout),  # 退出登录
]
