from django.urls import path
from .  import views

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/info/', views.product_info, name='product_info'),
    path('products/<int:product_id>/', views.ProductRetrieveAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view()),
]
