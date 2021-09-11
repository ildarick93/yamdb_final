from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from api.permissions import IsAdmin, IsSuperuser
from api_yamdb.settings import EMAIL_FROM, EMAIL_SUBJECT, EMAIL_TEXT

from .serializers import (EmailSerializer, TokenObtainLifetimeSerializer,
                          TokenRefreshLifetimeSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperuser | IsAdmin]

    @action(detail=False, methods=('GET', 'PATCH',),
            permission_classes=[IsAuthenticated, ])
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
        else:
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        password = str(get_random_secret_key())[:8]
        password_hash = make_password(password)
        serializer.save(password=password_hash, is_active=True)


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [AllowAny, ]

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        username = email.split('@')[0]
        password = str(get_random_secret_key())[:8]
        password_hash = make_password(password)
        send_mail(
            EMAIL_SUBJECT,
            EMAIL_TEXT.format(email=email, confirmation_code=password),
            EMAIL_FROM,
            [email],
            fail_silently=False,
        )
        serializer.save(
            username=username,
            password=password_hash,
            email=email,
            is_active=True
        )


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainLifetimeSerializer


class TokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshLifetimeSerializer
