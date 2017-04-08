from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from login_app.forms import LoginForm
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login_app_templates/login.html', 'authentication_form': LoginForm}, name = "login_page"),
	url(r'^logout/$', auth_views.logout, {'next_page': '/login'},name = "logout_page"),
]