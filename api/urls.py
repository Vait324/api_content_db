from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UsersViewSet,
                    send_confirmation_code, send_token)

v1_router = DefaultRouter()

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
v1_router.register(
    r'titles', TitleViewSet,
    basename='titles'
)
v1_router.register(
    r'categories', CategoryViewSet,
    basename='categories'
)
v1_router.register(
    r'genres', GenreViewSet,
    basename='genres'
)
v1_router.register(
    r'users', UsersViewSet,
    basename='users'
)

urlpatterns = [
    path(
        'v1/', include(v1_router.urls)
    ),
    path(
        'v1/auth/email/', send_confirmation_code, name='send_confirmation_code'
    ),
    path(
        'v1/auth/token/', send_token, name='send_token'
    ),
]
