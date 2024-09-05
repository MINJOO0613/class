from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view # @api_view(["GET", "POST"])  # 장고에서 제공하는 API 데코레이터 (FBV로 쓸 때 필요함)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Article, Comment
from .serializers import (
    ArticleSerializer, 
    ArticleDetailSerializer, 
    CommentSerializer
)

# [Article] CBV (Class Based View = 클래스형 뷰로 CRUD)

# Article 모든 게시물 조회 및 생성(Create)
class ArticleListAPIView(APIView):          # DRF CBV의 베이스 클래스
    # RESTful API를 custom하는 코드
    @extend_schema(
        tags=["Articles"],
        description="Article 목록 조회를 위한 API",
    )

    # Article 목록조회
    def get(self, request):
        articles = Article.objects.all()
        # 목록조회 같이 모든 게시물을 가지고 올때는, "many=True"가 필요
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


    # RESTful API를 custom하는 코드
    @extend_schema(
        tags=["Articles"],
        description="Article 생성을 위한 API",
        request=ArticleSerializer,
    )

    # Article 생성
    def post(self, request):
        # 데이터가 바인딩된 serializer을 생성(Article에 사용자가 적은 내용들이 반영)
        serializer = ArticleSerializer(data=request.data)
        # 유효하지 않을 경우 에러를 표시하기 위해, "raise_exception=True"가 필요
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # 게시물 생성 및 수정에서는 데이터 저장이 필요함
            # 201이라고 적는 것보다 조금 더 명시적으로 보기 위한 방법
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Article 상세게시물 조회 및 수정, 삭제(pk가 필요함)
class ArticleDetailAPIView(APIView):          # DRF CBV의 베이스 클래스
    # 상세조회 시 꼭 필요한 함수(아래에서 반복되는 함수는 따로 빼준다)
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    # Article 싱세조회
    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    # Article 수정
    def put(self, request, pk):
        # 유저인지 확인
        permission_classes = [IsAuthenticated]

        article = self.get_object(pk) # 게시물 update를 하기 위해선, 이전에 작성했던 내용이 있어야 하므로 serializer에 instance로 article을 가져온다
        serializer = ArticleDetailSerializer(
            article, data=request.data, partial=True) # 모델폼에 필드를 부분적으로 수정하고 싶다면 "partial=True"가 필요
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # 게시물 생성 및 수정에서는 데이터 저장이 필요함
            return Response(serializer.data)

    # Article 삭제
    def delete(self, request, pk):
        # 유저인지 확인
        permission_classes = [IsAuthenticated]

        article = self.get_object(pk)
        article.delete()
        data = {"pk": f"{pk} article is deleted."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)



# [Comment] CBV (Class Based View = 클래스형 뷰로 CRUD)
class CommentListAPIView(APIView):
    # 댓글 조회
    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # 댓글 생성
    def post(self, request, article_pk):
        # 유저인지 확인
        permission_classes = [IsAuthenticated]

        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data) # 데이터가 바인딩된 serializer을 생성(Comment에 사용자가 적은 내용들이 반영)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article) # 저장할 때, article 정보도 있어야 됨. validated_data = {**self.validated_data, **kwargs}
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    # 댓글 수정
    def put(self, request, comment_pk):
        # 유저인지 확인
        permission_classes = [IsAuthenticated]

        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # 댓글 삭제
    def delete(self, request, comment_pk):  # comment_pk는 댓글의 id값
        # 유저인지 확인
        permission_classes = [IsAuthenticated]

        comment = self.get_object(comment_pk)
        comment.delete()
        data = {"pk": f"{comment_pk} comment is deleted."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
