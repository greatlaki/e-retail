from rest_framework import serializers
from provider.models.contact import Contact
from provider.models.provider import Provider


class ContactCreateSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())

    class Meta:
        model = Contact
        fields = ('email', 'country', 'city', 'street', 'house_no', 'provider')
