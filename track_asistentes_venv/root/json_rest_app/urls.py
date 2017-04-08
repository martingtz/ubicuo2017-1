from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^json_rest/', views.json_rest, name = 'test'),
]