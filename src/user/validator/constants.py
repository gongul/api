
from common.validator.constants import BaseValidationMessage


class Email(BaseValidationMessage):
    unique = '이미 존재하는 이메일입니다.'
    required = '이메일을 입력해주세요.'
    blank = '이메일을 입력해주세요.'
    max_length = '이메일은 255글자 이하로 입력해주세요.'


class Password(BaseValidationMessage):
    required = '비밀번호를 입력해주세요.'
    blank = '비밀번호를 입력해주세요.'
    max_length = '비밀번호는 128글자 이하로 입력해주세요.'
    min_length = '비밀번호는 8글자 이상으로 입력해주세요.'
    invalid = '패스워드가 형식이 올바르지 않습니다.'


class PhoneNumber(BaseValidationMessage):
    required = '전화번호를 입력해주세요.'
    blank = '전화번호를 입력해주세요.'
    invalid = '전화번호 형식이 올바르지 않습니다.'


class IsVerified(BaseValidationMessage):
    required = '계정 인증 여부를 입력해주세요.'
    blank = '계정 인증 여부를 입력해주세요.'
    invalid = '계정 인증 여부가 올바르지 않습니다.'


class IsActivated(BaseValidationMessage):
    required = '계정을 활성화/비활성화 시킬지 입력해주세요.'
    blank = '계정을 활성화/비활성화 시킬지 입력해주세요.'
    invalid = '계정을 활성화 여부가 올바르지 않습니다.'


class Name(BaseValidationMessage):
    required = '이름을 입력해주세요.'
    blank = '이름을 입력해주세요.'
    max_length = '이름은 50글자 이하로 입력해주세요.'


class NickName(BaseValidationMessage):
    required = '닉네임을 입력해주세요.'
    blank = '닉네임을 입력해주세요.'
    max_length = '닉네임은 50글자 이하로 입력해주세요.'
