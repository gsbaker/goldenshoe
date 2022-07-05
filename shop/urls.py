from django.urls import path
from django.views.generic import TemplateView

from shop import views

urlpatterns = [
    path('', views.index, name='index')
]
