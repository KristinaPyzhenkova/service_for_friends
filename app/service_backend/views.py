import json

from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action, permission_classes, api_view
from django.db.models import Q
from rest_framework import mixins
# from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from service_backend.models import User, Application, Friendship
from service_backend.serializers import (
    NewUserSerializer, ApplicationSerializer,
    ApplicationAcceptSerializer, FollowSerializer,
    StatusSerializer
)


@permission_classes([permissions.AllowAny, ])
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet предназначен для взаимодействия в моделью User.
    """
    queryset = User.objects.all()
    serializer_class = NewUserSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet предназначен для взаимодействия в моделью Application.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='send',
    )
    def application(self, request):
        user = get_object_or_404(User, username=request.user.username)
        applicant = get_object_or_404(User, username=self.request.data['applicant'])
        if Application.objects.filter(user=applicant, applicant=user).exists():
            profiles = Application.objects.filter(user=applicant, applicant=user).first()
            profiles.delete()
            Friendship.objects.create(user1=user, user2=applicant)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'You became friends.'
            }
            return Response(response)
        elif Application.objects.filter(user=user, applicant=applicant).exists():
            response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Application with this user and applicant already exists."
            }
            return Response(response)
        elif user == applicant:
            response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "You can't add yourself as a friend."
            }
            return Response(response)
        elif (
            Friendship.objects.filter(user1=user, user2=applicant).exists() or
            Friendship.objects.filter(user2=user, user1=applicant).exists()
        ):
            response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "You are already friends."
            }
            return Response(response)
        else:
            serializer = ApplicationSerializer(data={'user': user, 'applicant': applicant})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, applicant=applicant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='incoming',
    )
    def application_incoming(self, request):
        try:
            application = Application.objects.filter(applicant=request.user)
            serializer = ApplicationSerializer(application, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='outgoing',
    )
    def application_outgoing(self, request):
        try:
            application = Application.objects.filter(user=request.user)
            serializer = ApplicationSerializer(application, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ApplicationAcceptViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationAcceptSerializer

    def update(self, request, username):
        try:
            user = get_object_or_404(User, username=username)
            applicant = get_object_or_404(User, username=request.user.username)
            accept = self.request.data['accept']
            serializer = ApplicationAcceptSerializer(data={'user': user, 'applicant': applicant, 'accept': accept})
            serializer.is_valid(raise_exception=True)
            profiles = Application.objects.filter(user=user, applicant=applicant).first()
            if not profiles:
                response = {
                    'status': 'success',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'There are no such requests to accept / reject - send a request first.'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data['accept']:
                profiles.delete()
                Friendship.objects.create(user1=user, user2=applicant)
                response = {
                    'status': 'success',
                    'code': status.HTTP_201_CREATED,
                    'message': 'You became friends.'
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                profiles.delete()
                response = {
                    'status': 'success',
                    'code': status.HTTP_201_CREATED,
                    'message': 'Application rejected.'
                }
                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'status': 'success',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'The request is incorrect.'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class FriendshipViewSet(viewsets.ModelViewSet):
    """
        ViewSet предназначен для взаимодействия в моделью Friendship.
        """
    queryset = Friendship.objects.all()
    serializer_class = FollowSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        self.queryset = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        return super().list(request, *args, **kwargs)

    def update(self, request, username):
        user = request.user
        queryset = Friendship.objects.filter(
            (Q(user1__username=username) & Q(user2=user)) |
            (Q(user1=user) & Q(user2__username=username))
        ).first()
        if queryset:
            queryset.delete()
            response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": f"You unfriended user {username}."
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        else:
            response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": f"You don't have this user as a friend."
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class FriendshipStatusViewSet(viewsets.ViewSet):
    """
    ViewSet для получения статуса дружбы и заявок.
    """
    def retrieve(self, request, username=None):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            response = {
                'status': 'error',
                'message': 'Указанное имя пользователя не существует.'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = StatusSerializer(username, context={'request': request})
        status_friend = serializer.data['status']

        response = {
            'username': username,
            'status': status_friend
        }

        return Response(response, status=status.HTTP_200_OK)


