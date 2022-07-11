
from common.validator.constants import BaseValidationMessage


class CertificationNumber(BaseValidationMessage):
    required = '인증번호를 입력해주세요.'
    max_value = '인증번호가 올바르지 않습니다.'
    min_value = '인증번호가 올바르지 않습니다.'
    invalid = '인증번호가 올바르지 않습니다.'
    expired = '인증번호를 다시 받아주세요.'
