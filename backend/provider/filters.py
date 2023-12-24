import django_filters
from provider.models.provider import Provider


class IdFilterInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class ProviderFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='contacts__country', lookup_expr='icontains')
    product_ids = IdFilterInFilter(field_name='retail_products__id', lookup_expr='in')

    class Meta:
        model = Provider
        fields = ('country', 'product_ids')
