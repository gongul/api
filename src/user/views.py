from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from user.permissions import IsUserOwner

from .models import User
from .serializers import ResetPasswordSerializer, SignupSerializer, UserSerializer


@method_decorator(extend_schema(operation_id='유저 디테일'), name="get")
class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserOwner]


@method_decorator(extend_schema(operation_id='회원가입'), name="post")
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    authentication_classes = []


class ResetPasswordView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer
    authentication_classes = []

    @extend_schema(operation_id='비밀번호 초기화')
    def post(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)
