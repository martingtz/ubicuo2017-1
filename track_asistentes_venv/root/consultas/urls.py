from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^consulta/', views.consulta_form, name = 'consulta'),
]