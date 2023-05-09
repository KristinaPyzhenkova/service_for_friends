from rest_framework import serializers
from django.db.models import Q

from service_backend.models import User, Application, Friendship


class NewUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания новых пользователей.
    """

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ApplicationAcceptSerializer(serializers.ModelSerializer):
    accept = serializers.BooleanField(write_only=True, required=False)
    user = serializers.CharField(source='user.username', read_only=True)
    applicant = serializers.CharField(source='applicant.username', read_only=True)

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заявок.
    """
    user = serializers.CharField(source='user.username', read_only=True)
    applicant = serializers.CharField(source='applicant.username', read_only=True)

    class Meta:
        model = Application
        fields = (
            'id',
            'user',
            'applicant',
            'created_at',
        )


class FollowSerializer(serializers.ModelSerializer):
    """ Сериализация: список друзей. """
    user = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ('user',)

    def get_user(self, obj):
        user = self.context['request'].user
        if user == obj.user1:
            return obj.user2.username
        elif user == obj.user2:
            return obj.user1.username
        return None


class StatusSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()

    def get_status(self, username):
        request_user = self.context['request'].user
        try:
            user = User.objects.get(username=username)
            is_friend = Friendship.objects.filter(
                Q(user1=user, user2=request_user) | Q(user1=request_user, user2=user)).exists()
            has_incoming_request = Application.objects.filter(user=user, applicant=request_user).exists()
            has_outgoing_request = Application.objects.filter(user=request_user, applicant=user).exists()

            if is_friend:
                return 'Уже друзья'
            elif user == request_user:
                return 'Это ты!'
            elif has_incoming_request:
                return 'Входящая заявка'
            elif has_outgoing_request:
                return 'Исходящая заявка'
            else:
                return 'Нет ничего'
        except User.DoesNotExist:
            return 'Пользователь не найден'
