from django.shortcuts import render , get_object_or_404
from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny ,
    )
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import *
from .models import *
from .filters import *
from.pagination import *
from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination ,LimitOffsetPagination


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset= Product.objects.order_by('pk')
    serializer_class =  ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStoclFilterBackend,
        ]
    search_fields = ['name','description']
    ordering_fields = ['name', 'price']
    pagination_class = CustomPagination
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    @action(detail=False , methods=['get'] , url_path='user-orders' , permission_classes=[IsAuthenticated])
    def user_orders(self,request):
        orders = self.get_queryset().filter(user=request.user)
        serializer =self.get_serializer(orders,many=True)
        return Response(serializer.data)
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    def get(self,request):
        products = Product.objects.order_by('id')
        serializer = ProductInfoSerializer({
            'products':products,
            'count':len(products),
            'max_price':products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)