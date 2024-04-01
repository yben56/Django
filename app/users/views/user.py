from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import User
from ..serializers import UserSerializer


@api_view(['GET'])    
def user(request):
    user = User.objects.filter(id=request.userinfo['id']).first()
    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)