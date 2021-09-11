from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_users = DefaultRouter()
router_users.register('users', views.UserViewSet)

auth_patterns = [
    path('email/', views.UserRegisterView.as_view(),
         name='email'),
    path('token/', views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(),
         name='token_refresh'),
]

urlpatterns = [
    path('', include(router_users.urls)),
    path('auth/', include(auth_patterns)),
]
