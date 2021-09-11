from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register(r'genres', GenreViewSet, 'Genre')
router.register(r'categories', CategoryViewSet, 'Category')
router.register(r'titles', TitleViewSet, 'Title')
router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet)

urlpatterns = [
    path('v1/', include('users.urls')),
    path('v1/', include(router.urls)),
]
