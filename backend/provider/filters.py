import django_filters
from provider.models.provider import Provider


class ProviderFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='contacts__country', lookup_expr='icontains')
    product = django_filters.CharFilter(field_name='contacts__country', lookup_expr='icontains')

    class Meta:
        model = Provider
        fields = ('country',)
