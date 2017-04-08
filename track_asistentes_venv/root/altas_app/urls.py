from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^altas/', views.alta_form, name = 'altas_page'),
    url(r'^test/', views.get_name, name = 'test_page'),
]