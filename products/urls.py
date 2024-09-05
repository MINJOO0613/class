from django.urls import path
from . import views

app_name = "products"       #API에서는 앱네임, view 네임은 필요하지 않음(삭제해도 됨)
urlpatterns = [
    # path("", views.ProductListAPIView.as_view(), name="product_list"), # as_view() 메서드를 사용해서 URL패턴 연결, 호출 가능한 함수로 변환
    path("", views.product_list)
    # path("<int:pk>/", views.ProductDetailAPIView.as_view(), name="product_detail"),
]
