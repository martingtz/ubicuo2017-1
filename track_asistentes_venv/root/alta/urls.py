from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^alta/', views.alta_form, name = 'alta'),
]