from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.detail, name='detail'),
    path('basket/', views.basket, name='basket'),
    path('delete_basket_item/<int:basket_item_id>', views.basket_item_delete, name='delete-basket-item'),
    path('increment_basket_item/<int:basket_item_id>', views.increment_basket_item, name='increment-basket-item'),
    path('decrease_basket_item/<int:basket_item_id>', views.decrease_basket_item, name='decrease-basket-item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
