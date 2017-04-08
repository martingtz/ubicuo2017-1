from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^consultas/', views.consulta_form, name = 'consultas_page'),
]