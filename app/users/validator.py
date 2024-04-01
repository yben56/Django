from validator import Validator
from django.utils import timezone

class SignupValidator(Validator):
    first_name = 'required'
    last_name = 'required'
    email = 'required|email'
    password = 'required|min_length:8'
    birthday = f'required|date:%Y-%m-%d|date_before:{timezone.now().date()}'
    gender = 'required|boolean'

    message = {}

class EmailValidator(Validator):
    email = 'required|email'

class PasswordValidator(Validator):
    password = 'required|min_length:8'