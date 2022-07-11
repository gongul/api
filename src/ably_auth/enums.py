from django.db import models


class TokenType(models.IntegerChoices):
    ACCESS_TOKEN = 0, '엑세스 토큰'
    REFRESH_TOKEN = 1, '리프레쉬 토큰'
