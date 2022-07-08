from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from shop import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.detail, name='detail'),
    path('basket/', views.basket, name='basket'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
