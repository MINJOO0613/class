from django.shortcuts import render
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializers import (
    ProductSerializer,
)

# class ProductListAPIView(APIView):
#     # Product 목록조회
#     def get(self, request):
#         products = Product.objects.all()
#         # 목록조회 같이 모든 게시물을 가지고 올때는, "many=True"가 필요
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)


@api_view(["GET"])
def product_list(request):
    cache_key = "product_list"

    if not cache.get(cache_key):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        json_response = serializer.data
        cache.set(cache_key, json_response, 180)

    json_response = cache.get(cache_key)
    return Response(json_response)