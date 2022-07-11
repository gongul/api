from random import randint
from django.urls import reverse
from rest_framework.test import APITestCase

from user.tests import UserFactory, JwtTokenGenerator

from .serializers import SmsCertificationNumber


class SmsTestCase(APITestCase):
    ''' SMS 인증 번호 관련 API 테스트 클래스 '''

    def setUp(self):
        self.phone_number = '010-0000-0000'

    def test_send_sms_certification_number(self):
        ''' sms 인증 번호 발송 API 테스트 '''
        url = reverse('auth-send-sms-certification_number')
        response = self.client.post(url, {'phone_number': self.phone_number})

        self.assertEqual(201, response.status_code)

    def test_verify_sms_certification_number(self):
        ''' sms 인증 번호 검증 API 테스트 '''
        url = reverse('auth-verify-sms-certification_number')
        certification_number = SmsCertificationNumber.create(self.phone_number)
        response = self.client.post(url, {'phone_number': self.phone_number,
                                          'certification_number': certification_number})

        self.assertEqual(200, response.status_code)


class JwtTokenTestCase(APITestCase):
    ''' 토큰 관련 API 테스트 클래스 '''

    def setUp(self):
        self.plain_password = 'test123456789'
        self.user = UserFactory.create(password=self.plain_password)

    def test_create_token(self):
        ''' 토큰 발급 API 테스트 '''
        url = reverse('auth-create-token')
        response = self.client.post(url, {'email': self.user.email,
                                          'password': self.plain_password})

        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.data.get('access_token'))

    def test_verify_token(self):
        ''' 토큰 검증 API 테스트 '''
        url = reverse('auth-verify-token')
        access_token = JwtTokenGenerator().create_access_token(self.user.email)
        refresh_token = JwtTokenGenerator().create_refresh_token(self.user.email)
        response = self.client.post(url, {'access_token': access_token,
                                          'refresh_token': refresh_token})

        self.assertEqual(200, response.status_code)
        self.assertEqual(access_token, response.data.get('access_token'))
        self.assertEqual(refresh_token, response.data.get('refresh_token'))

    def test_refresh_token(self):
        ''' 토큰 재발급 API 테스트 '''
        url = reverse('auth-refresh-token')
        refresh_token = JwtTokenGenerator().create_refresh_token(self.user.email)
        response = self.client.post(url, {'refresh_token': refresh_token})

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data.get('access_token'))
