from django.urls import path
from . import views

app_name = "articles"       #API에서는 앱네임, view 네임은 필요하지 않음(삭제해도 됨)
urlpatterns = [
    path("", views.ArticleListAPIView.as_view(), name="article_list"), # as_view() 메서드를 사용해서 URL패턴 연결, 호출 가능한 함수로 변환
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:article_pk>/comments/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("comments/<int:comment_pk>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),
]
