from rest_framework import serializers
from .models import Book, User, Review, Banner

class SimpleSerializer(serializers.Serializer):
    content = serializers.JSONField()
    
class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class AccountSerializer(serializers.Serializer):
    token = serializers.CharField()
    nickname = serializers.CharField()
    is_first = serializers.BooleanField()

class ReviewSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    read_state = serializers.CharField()
    score = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    content = serializers.CharField()

class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    keywords = serializers.StringRelatedField(many=True, read_only=True, required=False)
    class Meta:
        model = Book
        fields = ('id', 'image', 'title', 'subtitle', 'isbn', 'author', 'publisher', 'pubdate', 'genre', 'intro', 'desc', 'desc_pub', 'desc_index', 'category', 'kdc', 'keywords', 'num_review')
        read_only_fields = ('id',)

class BookSimpleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    keywords = serializers.StringRelatedField(many=True, read_only=True, required=False)
    class Meta:
        model = Book
        fields = ('id', 'image', 'title', 'subtitle', 'isbn', 'author', 'publisher', 'pubdate', 'keywords')
        read_only_fields = ('id',)
        
class ReviewDetailSerializer(serializers.ModelSerializer):
    book = BookSimpleSerializer()
    user_name = serializers.CharField()
    read_state = serializers.CharField()
    score = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    content = serializers.CharField()
    
    class Meta:
        model = Review
        fields = ('id', 'book', 'user_name', 'read_state', 'score', 'created_at', 'content')
        read_only_fields = ('id',)
    
    @classmethod
    def from_model(cls, review: Review):
        return cls(dict(
            book=BookSimpleSerializer(review.book).data,
            user_name=review.user.nickname,
            read_state=review.read_state,
            score=review.score,
            created_at=review.created_at,
            content=review.content
        ))

class BookDetailSerializer(serializers.Serializer):
    book = BookSerializer()
    my_review = ReviewSerializer()
    similar = BookSimpleSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    
class BookLineSerializer(serializers.Serializer):
    title = serializers.CharField()
    books = BookSimpleSerializer(many=True)
    
class MainSerializer(serializers.Serializer):
    banner = BookDetailSerializer(many=True)
    lines = BookLineSerializer(many=True)
    
class SearchSerializer(serializers.Serializer):
    books = BookSimpleSerializer(many=True)
    count = serializers.IntegerField()
    
class BannerSerializer(serializers.ModelSerializer):
    book = BookSimpleSerializer()
    keywords = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = Banner
        fields = ('book', 'color1', 'color2', 'content', 'order', 'keywords')
    

# 리뷰 시리얼라이저는 유저정보도 담기
# 책 detail에 리뷰 넣기