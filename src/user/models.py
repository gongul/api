from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db import models

from user.validator.message import UserValidationMessage


class UserManager(BaseUserManager):
    def create_user(self, email, name, nickname, phone_number, password, registration_date=None, is_activated=False, is_verified=False):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            nickname=nickname,
            phone_number=phone_number,
            registration_date=registration_date,
            is_activated=is_activated,
            is_verified=is_verified
        )

        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.AutoField('아이디', primary_key=True)
    email = models.EmailField('이메일', unique=True, max_length=255, error_messages=UserValidationMessage.EMAIL.to_dict())
    password = models.CharField('패스워드', max_length=128, error_messages=UserValidationMessage.PASSWORD.to_dict())
    phone_number = models.CharField('전화번호', max_length=20, error_messages=UserValidationMessage.PHONE_NUMBER.to_dict())
    name = models.CharField('이름', max_length=50, error_messages=UserValidationMessage.NAME.to_dict())
    nickname = models.CharField('닉네임', max_length=50, error_messages=UserValidationMessage.NICKNAME.to_dict())
    registration_date = models.DateTimeField('회원가입 일시', auto_now_add=True, blank=True)
    is_verified = models.BooleanField('인증 여부', default=False, blank=True, error_messages=UserValidationMessage.IS_VERIFIED.to_dict())
    is_activated = models.BooleanField('활성화 여부', default=False, blank=True, error_messages=UserValidationMessage.IS_ACTIVATED.to_dict())

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'
