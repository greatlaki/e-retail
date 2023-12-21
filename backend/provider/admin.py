from provider.models.providers import Provider
from provider.models.contacts import Contact
from provider.models.products import Product
from django.contrib import admin

admin.site.register(Contact)
admin.site.register(Product)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name',)
    list_filter = ('contacts__city',)
