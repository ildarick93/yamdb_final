from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .permissions import IsAdmin, IsModerator, IsOwner, IsSuperuser, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleReaderSerializer)

User = get_user_model()


class ListCreateDestroyMixin(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = [IsAdmin | IsSuperuser | ReadOnly]


class CategoryViewSet(ListCreateDestroyMixin):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('slug',)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class GenreViewSet(ListCreateDestroyMixin):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('slug',)
    search_fields = ['=name', '=slug']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = [IsAdmin | IsSuperuser | ReadOnly]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateSerializer
        return TitleReaderSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated | ReadOnly,
                          IsOwner | IsAdmin | IsModerator | ReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        title_id = title.id
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title = int(self.kwargs.get("title_id"))
        title_obj = get_object_or_404(Title, id=title)
        serializer.save(
            author=self.request.user,
            title=title_obj)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated | ReadOnly,
                          IsOwner | IsAdmin | IsModerator | ReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        review_id = review.id
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user,
                        review_id=review)
