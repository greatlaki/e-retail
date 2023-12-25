from decimal import Decimal

from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from provider.models.provider import Provider
from provider.models.contact import Contact
from provider.models.product import Product
from django.contrib import admin, messages

from provider.tasks import clear_debt_task

admin.site.register(Contact)
admin.site.register(Product)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name', 'view_provider_link')
    list_filter = ('contacts__city',)

    actions = ['pay_off_debt_owed']

    def view_provider_link(self, obj):
        if obj.provider is None:
            return ' - '

        url = reverse('admin:provider_provider_change', args=[obj.provider.pk])
        return format_html('<a href="{}">{}</a>'.format(obj.provider.id, obj.provider.name), url)

    @admin.action(description='Pay off the debt owed to the provider')
    def pay_off_debt_owed(self, request, queryset):
        if len(queryset) > 20:
            updated = clear_debt_task.delay(list(queryset.values_list('id', flat=True)))
        else:
            updated = queryset.update(debt=Decimal('0.0'))
        self.message_user(
            request,
            ngettext(
                '%d debt was successfully paid off.',
                '%d debts were successfully paid off.',
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
