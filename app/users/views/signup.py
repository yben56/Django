from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..validator import SignupValidator
from django.contrib.auth.hashers import make_password

from ..models import User
from ..serializers import UserSerializer

from .email_confirmation import sendmail

@api_view(['POST'])
def signup(request):
    #1. validator
    validator = SignupValidator(request.data)
    
    if validator.validate() == False:
        return Response(validator.get_message(), status=status.HTTP_400_BAD_REQUEST)

    #2. user exist or not
    user = User.objects.filter(email=request.data.get('email')).first()

    if user:
        #3. user is_not_active
        if user.is_active == 0:
            return Response({'error' : 'This email address has been registered but hasn not been confirmed yet. Please reconfirm your email'}, status=status.HTTP_400_BAD_REQUEST)

        #4. email exists
        else:
            return Response({'error' : 'This email address is already in use'}, status=status.HTTP_400_BAD_REQUEST)
    
    #5. password encrypt
    request.data._mutable = True
    request.data['password'] = make_password(request.data.get('password'))

    #6. serializer
    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #7. insert db
    user = User.objects.create(**serializer.validated_data)

    #8. send confirmation email
    email = sendmail(user.id, [user.email])

    if email:
        return Response({'error' : email}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)