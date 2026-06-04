from django.shortcuts import render , get_object_or_404
from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny ,
    )
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import *
from .models import *
from .filters import *
from rest_framework import filters 
from django_filters.rest_framework import DjangoFilterBackend


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset= Product.objects.all()
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
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    def get(self,request):
        products = Product.objects.order_by('id')
        serializer = ProductInfoSerializer({
            'products':products,
            'count':len(products),
            'max_price':products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)