from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.response import Response

from user_api.serializers import UserSerializer, EmailAuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    """update an existing user in the system"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """:return request.user"""
        user = None
        if self.request and hasattr(self.request, "user"):
            user = self.request.user
        return user


class DeactivateUserView(generics.DestroyAPIView):
    """deactivate an existing user in the system"""
    # serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """:return request.user"""
        user = None
        if self.request and hasattr(self.request, "user"):
            user = self.request.user
        return user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN, data='user deactivated')

    def perform_destroy(self, user):
        user.is_active = False
        user.save()


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = EmailAuthTokenSerializer
    # obtain_auth_token view explicitly uses JSON requests and responses,
    # rather than using default renderer and parser classes in your settings, link below.
    # https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
