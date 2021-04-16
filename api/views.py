from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.aggregates import Avg
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Categories, Comment, CustomUser, Genres, Review, Titles
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrModerator
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmationCodeSerializer, EmailSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleRatingSerializer, TitleSerializer,
                          UsersSerializer)


class CustomMixin(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerator, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Titles, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        return Comment.objects.filter(title=title, review=review).all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Titles, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, title=title, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerator, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        user = self.request.user
        serializer.save(author=user, title=title)


class CategoryViewSet(CustomMixin):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filterset_fields = ['name', ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleRatingSerializer
        return TitleSerializer


@api_view(['POST'])
def send_confirmation_code(request):
    if request.method == 'POST':
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.POST.get('email')
        user, state = CustomUser.objects.get_or_create(email=email)
        token = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation code!',
            message=str(token),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email, ]
        )
        return Response('Confirmation code отправлен на ваш Email.')


@api_view(['POST'])
def send_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = request.POST.get('confirmation_code')
    email = request.POST.get('email')
    user = get_object_or_404(CustomUser, email=email)
    if confirmation_code is None:
        return Response('Введите confirmation_code')
    if email is None:
        return Response('Введите email')
    token_check = default_token_generator.check_token(user, confirmation_code)
    if token_check is True:
        refresh = RefreshToken.for_user(user)
        return Response(f'Ваш токен:{refresh.access_token}')
    return Response('Неправильный confirmation_code или email.')


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    search_fields = ('user__username',)
    ordering = ('username',)

    @action(
        detail=False, methods=('get', 'patch',),
        url_path='me', url_name='me',
        permission_classes=[IsAuthenticated]
    )
    def get_me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.data)
