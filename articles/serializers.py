from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("article",) # 읽기전용 필드로 쓰겠다. (article의 정보가 있어야 is_valid를 통과할 수 있음.)
    

# 응답 구조만 변경하기
    def to_representation(self, instance):  # Serialization이후 보여지는 결과에 대해 자동으로 내부적으로 불리는 함수
        ret = super().to_representation(instance)
        ret.pop("article")
        return ret


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ArticleDetailSerializer(ArticleSerializer):           # 커스텀 필드 추가하기
    comments = CommentSerializer(many=True, read_only=True) # commets 라는 기존에 존재하는 매니저 이름으로 된 필드를 다시 override하는데 표현 방식은 CommentSerializer를 사용
    comments_count = serializers.IntegerField(source="comments.count", read_only=True) # article.comments.count() == comments.count