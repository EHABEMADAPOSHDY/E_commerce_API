from django.urls import path
from .  import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view(), name='product_info'),
    path('products/<int:product_id>/', views.ProductRetrieveAPIView.as_view()),
    path('user/',views.UserListView.as_view()),
]

routers = DefaultRouter()
routers.register('orders',views.OrderViewSet)
urlpatterns += routers.urls