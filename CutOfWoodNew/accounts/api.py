from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import Account

import sys
sys.path.append('../')
from products.serializers import CartSerializer


class RegisterAPI(generics.GenericAPIView):
    """ API для регистрации нового пользователя """

    def post(self, request, *args, **kwargs):
        newUser = RegisterSerializer(data = request.data)
        newUser.is_valid(raise_exception = True)

        user = newUser.save()

        if user:
            newCart = CartSerializer(data={'user': user.id, 'price': 0})
            newCart.is_valid(raise_exception = True)
            newCart.save()

        return Response({
            "user": UserSerializer(user, context = self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    """ API для авторизации пользователя """
    
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context = self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })



class UserAPI(generics.RetrieveAPIView):
    """ API для получения информации об авторизованном пользователе """

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user