import datetime
from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory
import factory

from faker import Faker


from provider.models.provider import Provider
from provider.models.contact import Contact
from provider.models.product import Product

fake = Faker(locale='en_Us')


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


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    email = factory.Faker('email')
    country = fake.country()
    city = fake.city()
    street = fake.street_name()
    house_no = fake.building_number()

    provider = SubFactory(ProviderFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = fuzzy.FuzzyText(prefix='test-')
    model = fuzzy.FuzzyText(prefix='test-')
    first_date_of_release = fuzzy.FuzzyDate(start_date=datetime.date(2007, 1, 1))

    provider = SubFactory(ProviderFactory)
