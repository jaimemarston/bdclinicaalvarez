# Create your views here.
import jwt
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from citas.serializer import UserSerializer, GroupSerializer, CitasSerializer,AuthenticationUserSerializer,UserSerializer
from rest_framework import generics
from .models import Citas,Usuarios

from django.contrib.auth import user_logged_in
from django.shortcuts import render
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_jwt.utils import jwt_payload_handler

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from rest_framework import serializers, viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CitasViewSet(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = CitasSerializer

#class CitasList(generics.ListAPIView):
#    queryset = Citas.objects.all()
#    serializer_class = CitasSerializer

class CitasList(generics.ListCreateAPIView):
    queryset = Citas.objects.all()
    serializer_class = CitasSerializer


class CitasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Citas.objects.all()
    serializer_class = CitasSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = Usuarios.objects.all()


class Authenticate(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(methods=['POST'], detail=False, url_path='obtain_token')
    def obtain_token(self, request):
        try:
            SECRET_KEY = 'l*)bi@k9_(ri0s&mxsz^-doolu&y_k@(zunqupdf=^c13cw73b'
            username = request.data['username']
            password = request.data['password']
            try:
                user = Usuarios.objects.get(username=username)
                pwd_valid = password == user.password
                if pwd_valid is False:
                    user = None
            except Usuarios.DoesNotExist:
                user = None
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, SECRET_KEY)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(AuthenticationUserSerializer(user).data,
                                    status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)

        except KeyError:
            res = {'error': 'please provide a email and password'}
            return Response(res)
