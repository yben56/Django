from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from ..validator import EmailValidator
import jwt
from ..models import User

@api_view(['GET', 'POST'])
def email_confirmation(request):
    #user click links from his/her email & confirm his/her account
    if request.method == 'GET':
        #1. token
        token = request.GET.get('token')

        if not token:
            return HttpResponse('Unauthenticated', status=403)

        #2. decode
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({ 'error' : 'Token expired' }, status=status.HTTP_403_FORBIDDEN) 
        except jwt.DecodeError:
            return Response({ 'error' : 'Unauthenticated' }, status=status.HTTP_403_FORBIDDEN) 

        #3. update db
        User.objects.filter(id=payload['id']).update(is_active=1)

        #4. response
        return Response(payload, status=status.HTTP_200_OK)  
    
    #use for resend Email Confirmation
    if request.method == 'POST':

        #1. validation
        validator = EmailValidator(request.data)

        if validator.validate() == False:
            return Response(validator.get_message(), status=status.HTTP_400_BAD_REQUEST)
        
        #2. get user
        user = User.objects.filter(email=request.data.get('email'), is_active=0).first()
        if not user:
            return Response({'error' : 'Could not find this email address'}, status=status.HTTP_400_BAD_REQUEST)

        #3. user only can request once every 60min


        #4. 
        email = sendmail({
            'id' : user.id,
            'subject' : 'Please confirm your email',
            'message' : 'Please confirm your email by clicking on the following link: http://127.0.0.1:8000/users/email_confirmation/',
            'from_email' : 'benjamin-w@hotmail.com',
            'recipient_list' : [user.email]
        })

        if email:
            return Response({'error' : email}, status=status.HTTP_400_BAD_REQUEST)

        #5. respose
        return Response(status=status.HTTP_200_OK)

    
def sendmail(options):
    try:
        #1. jwt token
        payload = {
            'id' : options['id'],
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        #2. links
        options['message'] = f'{options['message']}?token={token}'

        #3. send mail
        subject = options['subject']
        message = options['message']
        #from_email = 'noreply@word-z.com.tw'
        from_email = options['from_email']
        recipient_list = options['recipient_list']

        send_mail(subject, message, from_email, recipient_list)

        return False
    except Exception as e:
        return str(e)