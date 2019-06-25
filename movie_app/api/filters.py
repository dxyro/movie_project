import django_filters


class MovieFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    release_date = django_filters.DateFromToRangeFilter()

