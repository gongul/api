from django.urls import path

from . import views

user_patterns = ([
    path('users/<int:pk>', views.UserRetrieveView.as_view(), name='user-detail'),
    path('users/signup', views.SignupView.as_view(), name='user-signup'),
    path('users/<int:pk>/reset-password', views.ResetPasswordView.as_view(), name='user-reset-password'),
])
