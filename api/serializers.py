from rest_framework import serializers

from .models import Categories, Comment, CustomUser, Genres, Review, Titles


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id', 'text', 'author',
            'pub_date',
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id', 'text', 'author',
            'score', 'pub_date',
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return GenreSerializer(value).data


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return CategorySerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = '__all__'
        lookup_field = ('pk',)
        model = Titles


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'slug',
        )
        lookup_field = ('slug',)
        model = Genres


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'slug',
        )
        lookup_field = ('slug',)
        model = Categories


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name', 'last_name',
            'username', 'bio',
            'email', 'role',
        )
        model = CustomUser


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TitleRatingSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    rating = serializers.FloatField()

    class Meta:
        fields = (
            'id', 'name', 'year',
            'genre', 'rating',
            'category', 'description',
        )
        read_only_fields = (
            'id', 'rating',
        )
        model = Titles
