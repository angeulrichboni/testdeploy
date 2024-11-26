from http.client import responses

from rest_framework.permissions import AllowAny

from .serializers import SignUpSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user
# Create your views here.
# class SignUpView(generics.CreateAPIView):
#     serializer_class = SignUpSerializer
class SignUpView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self,request:Request):
        data=request.data
        serializer=self.serializer_class(data=data)

        if serializer.is_valid():
            user=serializer.save()

            response = {
                "message": "User Created with success",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request:Request):
        email=request.data.get('email')
        password=request.data.get('password')

        user=authenticate(email=email, password=password)

        if user is not None:
            tokens=create_jwt_pair_for_user(user)
            response={"message":"Login succesfuly", 'tokens':tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={"message":"Email or Password invalid"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request:Request):
        content={
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(data=content, status=status.HTTP_200_OK)