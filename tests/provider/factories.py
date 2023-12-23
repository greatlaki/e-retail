from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory
import factory

from provider.models.provider import Provider


class ProviderFactory(DjangoModelFactory):
    class Meta:
        model = Provider

    name = factory.Sequence(lambda n: 'provider %d' % n)
    provider = None
    debt = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    level = fuzzy.FuzzyInteger(low=0, high=4)


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Provider

    name = factory.Sequence(lambda n: 'provider %d' % n)
    provider = SubFactory(ProviderFactory)
    debt = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    level = fuzzy.FuzzyInteger(low=0, high=4)
