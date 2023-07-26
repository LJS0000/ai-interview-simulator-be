from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, CustomAuthTokenSerializer
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    # 각각의 메소드에 대해 권한을 지정
    permission_classes_by_action = {
        'create': [AllowAny],
        'login': [AllowAny],
        'logout': [IsAuthenticated],
        'default': [IsAuthenticated],
    }

    # 행동에 따라 permission_classes를 할당
    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [
                permission()
                for permission in self.permission_classes_by_action['default']
            ]

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response(
                {"error": "이메일과 비밀번호를 모두 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 사용자를 검증
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # 로그인 실패 시 에러 반환
        if not token:
            return Response(
                {"error": "이메일과 비밀번호를 확인해주세요."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response({'token': token.key})

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.auth.delete()
        return Response({"message": "성공적으로 로그아웃되었습니다."}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if password is not None:
            try:
                validate_password(password)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # serializer가 유효하다면, 사용자를 생성
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
