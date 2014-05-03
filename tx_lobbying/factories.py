import datetime
import random

import factory
import names

from . import models
from .models import (
    Interest,
    Lobbyist,
    LobbyistAnnum,
    Compensation,
    RegistrationReport,
    Coversheet,
)


class AddressFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Address
    state = u'TX'


class InterestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Interest

    name = factory.Sequence(lambda n: 'Interest {0}'.format(n))
    address = factory.SubFactory(AddressFactory)


class LobbyistFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Lobbyist
    filer_id = factory.Sequence(lambda n: n)
    updated_at = factory.LazyAttribute(lambda a: datetime.date.today())
    first_name = factory.LazyAttribute(lambda a: names.get_first_name())
    last_name = factory.LazyAttribute(lambda a: names.get_last_name())
    sort_name = factory.LazyAttribute(lambda a: "%s %s" % (
        a.last_name, a.first_name))
    address = factory.SubFactory(AddressFactory)


class LobbyistAnnumFactory(factory.DjangoModelFactory):
    FACTORY_FOR = LobbyistAnnum
    lobbyist = factory.SubFactory(LobbyistFactory)
    year = 2013


class CompensationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Compensation
    amount_high = factory.LazyAttribute(lambda a: random.randint(10000, 100000))
    amount_low = factory.LazyAttribute(lambda a: random.randint(0, a.amount_high))
    amount_guess = factory.LazyAttribute(lambda a: (a.amount_high + a.amount_low) / 2)
    annum = factory.SubFactory(LobbyistAnnumFactory)
    interest = factory.SubFactory(InterestFactory)
    updated_at = factory.LazyAttribute(lambda a: datetime.date.today())


class RegistrationReportFactory(factory.DjangoModelFactory):
    FACTORY_FOR = RegistrationReport
    lobbyist = factory.SubFactory(LobbyistFactory)
    report_id = factory.Sequence(int)
    report_date = '1970-01-01'
    year = 1970
    address = factory.SubFactory(AddressFactory)
    raw = '{}'


class CoversheetFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Coversheet
    lobbyist = factory.SubFactory(LobbyistFactory)
    report_date = '2001-04-01'
    report_id = factory.Sequence(lambda n: n)
    year = '2001'
    spent_guess = factory.LazyAttribute(lambda a: random.randint(10000, 100000))
