# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from .base import AppFigureObject

from .utils import as_int_or_none, as_decimal_or_none


class Pivot(object):
    PRODUCT = 'product'
    COUNTRY = 'country'
    DATE = 'date'
    STORE = 'store'


class Granularity(object):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

    @classmethod
    def allowed_values(cls):
        return (cls.DAILY, cls.WEEKLY, cls.MONTHLY, cls.YEARLY)

    @classmethod
    def validate(cls, value):
        if value not in cls.allowed_values():
            raise ParametersInvalid(
                '{} is not a valid granularity value. Allowed values: {}'.format(
                    value, cls.allowed_values()))


class ReportCollection(dict):
    GROUP_BY_FIELDS = (Pivot.PRODUCT,
                       Pivot.COUNTRY,
                       Pivot.DATE,
                       Pivot.STORE)


class SalesReport(AppFigureObject):
    """
    A simple sales report representation for appfigures.

    http://docs.appfigures.com/api/reference/v2/sales#Getting_Simple_Totals
    """

    def _load_from_json(self, json):
        # An int representing the total number of downloads.
        self.downloads = as_int_or_none(json.get('downloads'))

        # An int representing the number of downloads – returns.
        self.net_downloads = as_int_or_none(json.get('net_downloads'))

        # An int representing the total number of updates.
        self.updates = as_int_or_none(json.get('updates'))

        # A float representing the total revenue in the user’s selected
        # currency.
        self.revenue = as_decimal_or_none(json.get('revenue'))

        # An int representing the total number of returns.
        self.returns = as_int_or_none(json.get('returns'))

        self.edu_downloads = as_int_or_none(json.get('edu_downloads'))

        # An int representing the number of times products in this report were
        # gifted.
        self.gifts = as_int_or_none(json.get('gifts'))

        # An int representing the number of times products in this report were
        # gifted and then redeemed.
        self.gift_redemptions = as_int_or_none(json.get('gift_redemptions'))

        # An int representing the total number of promo codes used.
        self.promos = as_int_or_none(json.get('promos'))
