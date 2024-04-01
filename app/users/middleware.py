from django.http import HttpResponse
from rest_framework import status
import jwt

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return HttpResponse('Unauthenticated', status=403)
    
        try:
            #1. decode
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            #2. save user id after decode
            request.userinfo = payload
        except jwt.ExpiredSignatureError:
            return HttpResponse('Token expired', status=403)
        except jwt.DecodeError:
            return HttpResponse('Unauthenticated', status=403)

        response = self.get_response(request)
        return response