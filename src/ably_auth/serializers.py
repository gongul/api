from random import randint
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.fields import empty

from user.validator.message import UserValidationMessage
from common.redis import redis_client

from .validator.message import AuthValidationMessage
from .enums import TokenType

import math
import jwt
import datetime


def get_unix_time(dt):
    timestamp = dt.timestamp()
    unix_time = math.trunc(timestamp)

    return unix_time


class JwtTokenGenerator():
    def create_access_token(self, email, token_header={}):
        exp = get_unix_time(timezone.localtime() + datetime.timedelta(minutes=30))

        token_header['email'] = email
        token_header['exp'] = exp
        token_header['type'] = TokenType.ACCESS_TOKEN

        return self.encode(token_header)

    def create_refresh_token(self, email, token_header={}):
        exp = get_unix_time(timezone.localtime() + datetime.timedelta(hours=12))

        token_header['email'] = email
        token_header['exp'] = exp
        token_header['type'] = TokenType.REFRESH_TOKEN

        return self.encode(token_header)

    def encode(self, payload):
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def decode(self, token):
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            return data
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('만료된 토큰입니다.')
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('잘못된 토큰입니다.')


class SmsCertificationNumber():
    @staticmethod
    def validate(phone_number, certification_number):
        redis_key = ':'.join(['sms', phone_number])
        redis_certification_number = redis_client.get(redis_key)

        if redis_certification_number is None:
            raise serializers.ValidationError({
                'certification_number': [exceptions.ErrorDetail(AuthValidationMessage.CERTIFICATION_NUMBER.expired, code='expired')]
            })
        elif int(redis_certification_number) != certification_number:
            raise serializers.ValidationError({
                'certification_number': [exceptions.ErrorDetail(AuthValidationMessage.CERTIFICATION_NUMBER.invalid, code='invalid')]
            })

    def delete(phone_number):
        redis_key = ':'.join(['sms', phone_number])
        redis_client.delete(redis_key)

    def create(phone_number):
        certification_number = randint(100000, 999999)
        redis_key = ':'.join(['sms', phone_number])
        redis_client.set(redis_key, certification_number, 600)

        return certification_number


class SendSmsCertificationNumberSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(required=True, regex=r'^\d{2,3}-\d{3,4}-\d{4}$', error_messages=UserValidationMessage.PHONE_NUMBER.to_dict(), write_only=True)
    certification_number = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        validated_data['certification_number'] = SmsCertificationNumber.create(validated_data['phone_number'])

        return validated_data


class VerifySmsCertificationNumberSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(required=True, regex=r'^\d{2,3}-\d{3,4}-\d{4}$', error_messages=UserValidationMessage.PHONE_NUMBER.to_dict(), write_only=True)
    certification_number = serializers.IntegerField()

    def validate(self, attrs):
        SmsCertificationNumber.validate(attrs['phone_number'], attrs['certification_number'])

        return attrs


class CreateJwtTokenSerializer(JwtTokenGenerator, serializers.Serializer):
    email = serializers.EmailField(max_length=255, write_only=True, error_messages=UserValidationMessage.EMAIL.to_dict())
    password = serializers.CharField(min_length=8, max_length=128, write_only=True,
                                     error_messages=UserValidationMessage.PASSWORD.to_dict())
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def authenticate(self, email, password):
        credentials = {
            'email': email,
            'password': password
        }
        user = authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed('로그인에 실패하셨습니다.')
        elif not user.is_activated:
            raise exceptions.AuthenticationFailed('비활성화 상태 혹은 인증되지 않은 계정입니다.')

        access_token = self.create_access_token(user.email, {'nickname': user.nickname, 'name': user.name, 'id': user.id})
        refresh_token = self.create_refresh_token(user.email)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def create(self, validated_data):
        tokens = self.authenticate(validated_data['email'], validated_data['password'])
        validated_data['access_token'] = tokens['access_token']
        validated_data['refresh_token'] = tokens['refresh_token']

        return validated_data


class VerifyJwtTokenSerializer(JwtTokenGenerator, serializers.Serializer):
    access_token = serializers.CharField(allow_blank=True, required=False)
    refresh_token = serializers.CharField(allow_blank=True, required=False)

    def validate_access_token(self, value):
        decode_data = self.decode(value)

        if decode_data['type'] != TokenType.ACCESS_TOKEN:
            raise serializers.ValidationError('토큰 타입이 access_token이 아닙니다.')

        return value

    def validate_refresh_token(self, value):
        decode_data = self.decode(value)

        if decode_data['type'] != TokenType.REFRESH_TOKEN:
            raise serializers.ValidationError('토큰 타입이 refresh_token이 아닙니다.')

        return value


class RefreshJwtTokenSerializer(JwtTokenGenerator, serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        decode_data = self.decode(attrs['refresh_token'])
        attrs['access_token'] = self.create_access_token(decode_data['email'])

        return attrs
