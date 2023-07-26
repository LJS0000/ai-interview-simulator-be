from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# AuthTokenSerializer username 기본 설정 변경
class CustomAuthTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'), email=email, password=password
            )
            if not user:
                msg = '이메일과 비밀번호를 확인해주세요.'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = '이메일과 비밀번호를 모두 입력해주세요.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
