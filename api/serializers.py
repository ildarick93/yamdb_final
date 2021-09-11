from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ['id']


class TitleReaderSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='id', read_only=True)
    review = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'title', 'review')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    title = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    def validate(self, attrs):
        method = self._kwargs.get('context').get('request').method
        if method == "POST":
            title = int(self._kwargs.get('context').get(
                'request').parser_context.get('kwargs').get('title_id'))
            user = self._kwargs.get('context').get('request').user
            if user.reviews.all().filter(title_id=title).exists():
                raise serializers.ValidationError('Review has been added')
        return attrs

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date', 'title']
        model = Review
