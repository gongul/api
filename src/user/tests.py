from random import randint
from django.urls import reverse
from rest_framework.test import APITestCase

from ably_auth.serializers import JwtTokenGenerator, SmsCertificationNumber
from .models import User

import factory


def random_phone_number(seq):
    ''' 랜덤 폰번호 생성'''
    min_number = seq + 0000
    max_number = 9999

    middle_number = str(randint(min_number, max_number)).zfill(4)
    end_number = str(randint(min_number, max_number)).zfill(4)

    return f'010-{middle_number}-{end_number}'


class UserFactory(factory.django.DjangoModelFactory):
    ''' 손쉽게 테스트 유저를 생성하기 위한 클래스 '''
    class Meta:
        model = User

    email = factory.sequence(lambda n: f'test{n}@test.com')
    name = factory.sequence(lambda n: f'테스터{n}')
    nickname = factory.sequence(lambda n: f'테스터-닉네임{n}')
    password = factory.PostGenerationMethodCall('set_password', 'test123456789')
    phone_number = factory.sequence(random_phone_number)
    is_activated = True
    is_verified = True


class SignupTestCase(APITestCase):
    ''' 회원가입 API 테스트 클래스 '''

    def setUp(self):
        self.plain_password = 'test123456789'
        self.user = UserFactory.build(is_activated=False, is_verified=False)
        self.url = reverse('user-signup')
        self.certification_number = SmsCertificationNumber.create(self.user.phone_number)

    def test_signup(self):
        ''' 회원가입 API 테스트 '''
        credentials = {
            'email': self.user.email,
            'name': self.user.name,
            'nickname': self.user.nickname,
            'password': self.plain_password,
            'phone_number': self.user.phone_number,
            'certification_number': self.certification_number
        }

        response = self.client.post(self.url, credentials)

        self.assertEqual(201, response.status_code)


class UserDetailTestCase(APITestCase):
    ''' /users/<id> 관련 API 테스트 클래스   '''

    def setUp(self):
        self.plain_password = 'test123456789'
        self.user = UserFactory.create(password=self.plain_password)
        self.other_user = UserFactory.create(password=self.plain_password)
        self.authorization()

    def authorization(self):
        ''' authorization 설정 설정 '''
        access_token = JwtTokenGenerator().create_access_token(self.user.email)
        authorization = ' '.join(['Bearer', access_token])
        self.client.credentials(HTTP_AUTHORIZATION=authorization)

    def test_my_info(self):
        ''' 내 정보 보기 API 확인 테스트'''
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_other_user_info(self):
        ''' 다른 유저 정보 접근 API 권한 확인 테스트'''
        url = reverse('user-detail', args=[self.other_user.id])
        response = self.client.get(url)

        self.assertEqual(403, response.status_code)

    def test_reset_password(self):
        ''' 패스워드 초기화 API 테스트'''
        url = reverse('user-reset-password', args=[self.user.id])
        certification_number = SmsCertificationNumber.create(self.user.phone_number)
        response = self.client.post(url, {'phone_number': self.user.phone_number,
                                          'certification_number': certification_number,
                                          'password': self.plain_password})

        self.assertEqual(204, response.status_code)
