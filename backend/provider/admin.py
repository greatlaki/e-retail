from django.urls import reverse
from django.utils.html import format_html
from provider.models.providers import Provider
from provider.models.contacts import Contact
from provider.models.products import Product
from django.contrib import admin

admin.site.register(Contact)
admin.site.register(Product)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name', 'view_provider_link')
    list_filter = ('contacts__city',)

    def view_provider_link(self, obj):
        if obj.provider is None:
            return ' - '

        url = reverse('admin:provider_provider_change', args=[obj.provider.pk])
        return format_html('<a href="{}">{}</a>'.format(obj.provider.id, obj.provider.name), url)
