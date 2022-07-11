from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_miem.serializers import InheritsModelSerializer

from ably_auth.serializers import SmsCertificationNumber
from ably_auth.validator.message import AuthValidationMessage

from .models import User
from .validator.message import UserValidationMessage


class UserSerializer(InheritsModelSerializer):
    class Meta:
        model = User
        exclude = ['is_verified', 'is_activated', 'password', 'last_login']


class ResetPasswordSerializer(InheritsModelSerializer):
    certification_number = serializers.IntegerField(min_value=100000, max_value=999999, write_only=True,
                                                    error_messages=AuthValidationMessage.CERTIFICATION_NUMBER.to_dict())
    phone_number = serializers.RegexField(write_only=True, regex=r'^\d{2,3}-\d{3,4}-\d{4}$',
                                          error_messages=UserValidationMessage.PHONE_NUMBER.to_dict())
    password = serializers.CharField(min_length=8, max_length=128, write_only=True,
                                     error_messages=UserValidationMessage.PASSWORD.to_dict())

    class Meta:
        model = User
        fields = ['password', 'phone_number', 'certification_number']

    def validate(self, attrs):
        SmsCertificationNumber.validate(attrs['phone_number'], attrs['certification_number'])

        return attrs

    def validate_password(self, value):
        password = make_password(value)

        return password

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.password = validated_data['password']
        instance.save()
        SmsCertificationNumber.delete(validated_data['phone_number'])

        return instance


class SignupSerializer(InheritsModelSerializer):
    certification_number = serializers.IntegerField(min_value=100000, max_value=999999, error_messages=AuthValidationMessage.CERTIFICATION_NUMBER.to_dict(), write_only=True)
    phone_number = serializers.RegexField(regex=r'^\d{2,3}-\d{3,4}-\d{4}$', error_messages=UserValidationMessage.PHONE_NUMBER.to_dict())
    password = serializers.CharField(min_length=8, max_length=128, write_only=True,
                                     error_messages=UserValidationMessage.PASSWORD.to_dict())

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'nickname', 'name', 'password', 'certification_number']

    def validate_password(self, value):
        password = make_password(value)

        return password

    def validate(self, attrs):
        SmsCertificationNumber.validate(attrs['phone_number'], attrs['certification_number'])

        attrs['is_verified'] = True
        attrs['is_activated'] = True

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('certification_number')
        instance = super().create(validated_data)
        SmsCertificationNumber.delete(validated_data['phone_number'])

        return instance
