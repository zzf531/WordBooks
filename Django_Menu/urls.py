from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('word.urls')),
    path('', include('login.urls')),
    url(r'^captcha', include('captcha.urls')),
]
