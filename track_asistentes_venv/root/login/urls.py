from django.conf.urls import url

from . import views
from django.contrib.auth.views import login
##from django.contrib.auth import logout
from django.contrib.auth.views import logout
urlpatterns = [
    url(r'^$', login,{'template_name':'login_template/login.html'} , name = 'login'),

    url(r'^logout', logout,{'template_name':'login_template/login.html'} , name = 'logout'),
]