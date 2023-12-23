from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory
import factory

from provider.models.provider import Provider


class ProviderFactory(DjangoModelFactory):
    class Meta:
        model = Provider

    name = fuzzy.FuzzyText(prefix='test-')
    debt = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    provider = None
    level = fuzzy.FuzzyInteger(low=0, high=4)


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Provider

    name = fuzzy.FuzzyText(prefix='test-')
    provider = SubFactory(ProviderFactory)
    debt = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    level = fuzzy.FuzzyInteger(low=0, high=4)
