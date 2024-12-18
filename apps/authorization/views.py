from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, LoginSerializer, ResendEmailSerializer
from .models import EmailConfirmation

class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Проверьте свою почту для подтверждения регистрации.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailAPIView(APIView):
    def get(self, request, token):
        confirmation = get_object_or_404(EmailConfirmation, token=token)
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()
        return Response({'message': 'Email успешно подтверждён! Теперь вы можете войти.'}, status=status.HTTP_200_OK)
    
class ResendEmailAPIView(GenericAPIView):
    serializer_class = ResendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Email has been resent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)