from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])    
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    return response