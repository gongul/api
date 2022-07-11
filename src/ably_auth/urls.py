from django.urls import path

from . import views

ably_auth_patterns = ([
    path('auth/token', views.CreateJwtTokenView.as_view(), name='auth-create-token'),
    path('auth/verify-token', views.VerifyJwtTokenView.as_view(), name='auth-verify-token'),
    path('auth/refresh-token', views.RefreshJwtTokenView.as_view(), name='auth-refresh-token'),
    path('auth/send-sms-certification-number', views.SendSmsCertificationNumberView.as_view(), name='auth-send-sms-certification_number'),
    path('auth/verify-sms-certification-number', views.VerifySmsCertificationNumberView.as_view(), name='auth-verify-sms-certification_number'),
])
