from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserRoles

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'detail': 'Entered email exists'})
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=UserRoles.choices,
        default='user'
    )

    class Meta:
        fields = ['first_name', 'last_name',
                  'username', 'bio', 'email', 'role']
        model = User


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = serializers.CharField()
        del self.fields['password']

    def validate(self, attrs):
        attrs['password'] = attrs['confirmation_code']
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data
