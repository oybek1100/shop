from django.urls import path
from .views import index , add_product , delete_product , update_product , add_comment
from .views import product_detail , OrderDetail , expensive_product , cheap_product 
from . import views 

app_name = 'shop'


urlpatterns = [
    path('', index, name='index'), 
    path('detail/<int:product_id>/', views.product_detail, name='product_detail'), 
    path('category/<int:category_id>/', views.index, name='category_products'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('expensive_product/`', views.expensive_product, name='expensive_product'),
    path('cheap_product/`', views.cheap_product, name='cheap_product'),
    

]
