from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..validator import EmailValidator, PasswordValidator
from datetime import datetime, timedelta
import jwt

from ..models import User
from ..serializers import UserSerializer

@api_view(['POST'])
def login(request):
    #1. validator
    email_validator = EmailValidator(request.data)

    if email_validator.validate() == False:
        return Response(email_validator.get_message(), status=status.HTTP_400_BAD_REQUEST)
    
    password_validator = PasswordValidator(request.data)

    if password_validator.validate() == False:
        return Response(password_validator.get_message(), status=status.HTTP_400_BAD_REQUEST)
    
    #2. get user
    user = User.objects.filter(email=request.data['email']).first()

    #3. check email
    if user is None:
        return Response({'error' : 'Invalid Email or Password'}, status=status.HTTP_400_BAD_REQUEST)

    #4. check pwd
    if not user.check_password(request.data['password']):
        return Response({'error' : 'Invalid Email or Password'}, status=status.HTTP_400_BAD_REQUEST)
    
    #5. active
    if not user.is_active:
        return Response({'error' : 'This email address has been registered but has not been confirmed yet. Please reconfirm your email'}, status=status.HTTP_403_FORBIDDEN)

    #6. jwt
    payload = {
        'id' : user.id,
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow()
    }

    #7.
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)

    return response