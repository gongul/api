### 개발 스펙
- Redis
- Mysql
- Django (DRF)
- JWT
- Recommand Pypy 3.8 (`Cpython 3.8`,`Cpython 3.9`,`Pypy 3.8`,`Pypy 3.9` 작동 테스트 완료)

### 실행 방법
실행 하기 위해서는 `docker-compose`가 필수입니다. 

```
docker-compose -f docker-compose.yml up -d
```

### 실행 시 사용되는 포트는 아래와 같습니다.
- mysql : 7998
- redis : 7999
- api : 11111

### API 문서
`실행 방법`을 이용하여 서비스를 실행시키면 [Redoc](http://127.0.0.1:11111/docs/redoc), [Swagger](http://127.0.0.1:11111/docs/swagger) 문서를 통해 API 문서를 확인하실 수 있습니다.

### 라이브러리 설치
```
pip install -r requirements.txt
```

### 테스트 코드 실행
테스트 코드는 인수 테스트(API)에 집중하여 구현되어 있습니다. \
테스트 코드를 실행하기 위해서는 선행적으로 `실행 방법`,`라이브러리 설치`를 해야합니다. \
그 이후 아래 커맨드를 입력해주시면 됩니다.
```
python src/manage.py test --settings common.settings.local ./src/**/
```

### 구현된 범위 
- 회원가입 기능
- 내 정보 보기 기능
- 비밀번호 찾기 ( 재설정 ) 기능
- sms 인증 번호 발송 ( sms를 보내지 않기 때문에 인증번호를 response에 보냅니다)
- sms 인증 번호 검증
- jwt 토큰 발급 ( Bearer 방식의 인증 로그인 )
- jwt 토큰 검증
- jwt 토큰 재발급

### 신경쓴 부분
- github action을 이용한 ci 파이프 라인 구축
  - master branch push일 때 pypy3.8 unit test -> docker build & push
  - version branch push일 때 python version별 unit test 
- sms 인증 번호는 redis를 이용해서 구현
- API를 사용하는 사람들을 위한 Error Response 규격화
- 도커에서 실행되는 API gunicorn + gevent 비동기 처리가 blocking 없이 작동하도록 구성
   - `mysqlclient` mysqlclinet가 c 모듈로 되어 있어서 몽키 패치가 작동하지 않음
   - `cpython` + `pymysql` 쿼리 처리 속도 느림, non blocking 
   - `pypy + pymsql` 쿼리 처리 속도 빠름, non blocking 




