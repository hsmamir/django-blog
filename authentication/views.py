from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import (RegisterSerializer, LoginSerializer)


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
