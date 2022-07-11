from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import generics
from django.utils.decorators import method_decorator

from .serializers import CreateJwtTokenSerializer, RefreshJwtTokenSerializer, SendSmsCertificationNumberSerializer, VerifyJwtTokenSerializer, VerifySmsCertificationNumberSerializer


@method_decorator(extend_schema(operation_id='sms 인증 번호 발송'), name="post")
class SendSmsCertificationNumberView(generics.CreateAPIView):
    serializer_class = SendSmsCertificationNumberSerializer
    authentication_classes = []


class VerifySmsCertificationNumberView(generics.GenericAPIView):
    serializer_class = VerifySmsCertificationNumberSerializer
    authentication_classes = []

    @extend_schema(operation_id='sms 인증 번호 검증')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


@method_decorator(extend_schema(operation_id='토큰 발급'), name="post")
class CreateJwtTokenView(generics.CreateAPIView):
    serializer_class = CreateJwtTokenSerializer
    authentication_classes = []


class VerifyJwtTokenView(generics.GenericAPIView):
    serializer_class = VerifyJwtTokenSerializer
    authentication_classes = []

    @extend_schema(operation_id='토큰 검증')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class RefreshJwtTokenView(generics.GenericAPIView):
    serializer_class = RefreshJwtTokenSerializer
    authentication_classes = []

    @extend_schema(operation_id='토큰 재발급')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
