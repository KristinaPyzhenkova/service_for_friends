from rest_framework.routers import SimpleRouter
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

from service_backend.views import (
    ApplicationViewSet,
    UserViewSet,
    ApplicationAcceptViewSet,
    FriendshipViewSet,
    FriendshipStatusViewSet
)
from service_backend.yasg import urlpatterns as doc_urls


router = SimpleRouter()
router.register('new_user', UserViewSet, basename='user')
router.register('application', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.obtain_auth_token),
    path('application/<str:username>/', ApplicationAcceptViewSet.as_view(
        {'put': 'update'}), name='application-update'),
    path('friend/<str:username>/', FriendshipViewSet.as_view(
        {'put': 'update'}), name='friend-update'),
    path('friend/', FriendshipViewSet.as_view(
        {'get': 'list'}), name='friend'),
    path('status/<str:username>/', FriendshipStatusViewSet.as_view(
        {'get': 'retrieve'}), name='status'),

]
urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
