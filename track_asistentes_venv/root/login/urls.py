from django.conf.urls import url

from . import views
from django.contrib.auth.views import login
urlpatterns = [
    url(r'^login/', login,{'template_name':'login_template/login.html'} , name = 'login_page'),
    url(r'^test/', views.login_form, name = 'test'),
]