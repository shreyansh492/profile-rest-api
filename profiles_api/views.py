from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class HelloViewSet(viewsets.ViewSet):

    serializer_class= serializers.HelloSerializers

    def list(self,request):
        a_viewset = ['e','f','g']
        return Response({'messages': 'Hello !', 'a_viewset':a_viewset})

    def create(self,request):
        serializer= self.serializer_class(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        return Response({'method': 'get'})
    def update(self,request,pk=None):
        return Response({'method': 'PUT'})
    def partial_update(self,request,pk=None):
        return Response({'method': 'PATCH'})
    def destroy(self,request,pk=None):
        return Response({'method': 'DELETE'})

class HelloApiView(APIView):

    serializer_class= serializers.HelloSerializers
    def get(self,request,format=None):
        an_apiview=['a','b','c','d']

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self,request):
        serializer= self.serializer_class(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        return Response({'method': 'PUT'})
    def patch(self,request,pk=None):
        return Response({'method': 'PATCH'})
    def delete(self,request,pk=None):
        return Response({'method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializers
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
    permissions.UpdateOwnStatus,
    IsAuthenticated
    )

    def perform_create(self,serializer):
        serializer.save(user_profile = self.request.user)
