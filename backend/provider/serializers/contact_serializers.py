from rest_framework import serializers
from provider.models.contact import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'email', 'country', 'city', 'street', 'house_no')
