from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .email_confirmation import sendmail
from ..validator import EmailValidator, PasswordValidator
from ..models import User
import jwt
from django.contrib.auth.hashers import make_password

@api_view(['GET', 'POST', 'PUT'])
def reset_password(request):
     #user request forgot password
     if request.method == 'POST':
        #1. validation
        email_validator = EmailValidator(request.data)

        if email_validator.validate() == False:
            return Response(email_validator.get_message(), status=status.HTTP_400_BAD_REQUEST)

        #2. user should only request per hour!!!
        
        #3. get user
        user = User.objects.filter(email=request.data['email'], is_active=1).first()

        #4. check email
        if user is None:
            return Response({'error' : 'We could not find this account'}, status=status.HTTP_400_BAD_REQUEST)
 
        #5. send mail
        email = sendmail({
            'id' : user.id,
            'subject' : 'Reset Your Password',
            'message' : 'You are receiving this email because you requested to reset your password. If you did not make this request, you can ignore this email.\n\n' \
            'To reset your password, please click on the following link: http://127.0.0.1:8000/users/reset_password/',
            'from_email' : 'benjamin-w@hotmail.com',
            'recipient_list' : [user.email]
        })
        
        if email:
            return Response({'error' : email}, status=status.HTTP_400_BAD_REQUEST)

        #6. respose
        return Response(status=status.HTTP_200_OK)
     
     #user click reset password links
     if request.method == 'GET':
        #1. token
        token = request.GET.get('token')

        if not token:
            return Response({ 'error' : 'Unauthenticated' }, status=status.HTTP_403_FORBIDDEN) 

        #2. decode
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({ 'error' : 'Token expired' }, status=status.HTTP_403_FORBIDDEN) 
        except jwt.DecodeError:
            return Response({ 'error' : 'Unauthenticated' }, status=status.HTTP_403_FORBIDDEN) 

        #3. check user
        user = User.objects.filter(id=payload['id'], is_active=1).first()

        #4. response
        return Response(status=status.HTTP_200_OK)   
             
     #user update password
     if request.method == 'PUT':
        #1. token
        token = request.GET.get('token')

        if not token:
            return Response({ 'error' : 'Unauthenticated' }, status=status.HTTP_403_FORBIDDEN) 

        #2. decode
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({ 'error' : 'Token expired' }, status=status.HTTP_403_FORBIDDEN) 
        except jwt.DecodeError:
            return Response({ 'error' : 'Unauthenticated' }, status=status.HTTP_403_FORBIDDEN) 
        
        #3. password validator
        password_validator = PasswordValidator(request.data)

        if password_validator.validate() == False:
            return Response(password_validator.get_message(), status=status.HTTP_400_BAD_REQUEST)
        
        #4. password encrypt
        request.data._mutable = True
        pwd = make_password(request.data.get('password'))

        #5. update db
        User.objects.filter(id=payload['id']).update(password=pwd)

        return Response(status=status.HTTP_200_OK)