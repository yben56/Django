from rest_framework.response import Response
from rest_framework.decorators import api_view

#models & serializers
from .models import Item
from .serializers import ItemSerializer

#status
from rest_framework import status

#helper postman
from app.helpers import postman

@api_view(['GET'])
def getdata(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

    #items = {'name': 'ben', 'age': 26}
    #return Response(items)

@api_view(['POST'])
def adddata(request):
    serializer = ItemSerializer(data=request.data)

    if serializer.is_valid():
        #serializer.save()
        item = Item.objects.create(**serializer.validated_data)
    
        #return Response({serializer.data})
        return Response({}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def connectapi(request):
    response = postman('GET', 'https://fakestoreapi.com/products')
    return Response(response['body'], status=response['status'])

    #200 https://fakestoreapi.com/products
    #404 https://app.requestly.io/mock/7gmdFoaQdhKfe28uLfa9