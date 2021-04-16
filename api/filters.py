import django_filters as filters

from .models import Titles


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='contains'
    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )

    class Meta:
        model = Titles
        fields = '__all__'
