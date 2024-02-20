from rest_framework import status
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from notes_app.helpers.custom_authentication import EmailAuthBackend
from ..serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User


@api_view(['POST'])
def sign_up(request):
    try:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user=serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        print(exception)
        return Response({'message':'Something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        user=authenticate(username=email,password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as exception:
        return Response({'message':'Something went wrong','error':exception},status=status.HTTP_500_INTERNAL_SERVER_ERROR)