# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import six

from decimal import InvalidOperation, Decimal as D
from dateutil.parser import parse

from . import base


class ReviewCollection(list):

    def __init__(self, json):
        super(ReviewCollection, self).__init__()
        self.total = json.get('total', 0)
        self.pages = json.get('pages', 0)
        self.this_page = json.get('this_page', 0)

        for review_json in json.get('reviews', []):
            self.append(Review.from_json(review_json))

    @classmethod
    def from_json(cls, json):
        return cls(json)


class Review(base.AppFigureObject):
    SORT_FIELDS = ['country', 'stars', 'date']

    def _load_from_json(self, json):
        self.author = json.get('author')
        self.title = json.get('title')
        self.review = json.get('review')
        self.original_title = json.get('original_title')
        self.original_review = json.get('original_review')

        try:
            self.stars = D(json.get('stars'))
        except (TypeError, InvalidOperation):
            self.stars = None

        self.country_iso = json.get('iso')
        # Note: ISO is only available for iOS and Mac apps at this time.
        # Google Play does not support the concept of countries but rather
        # reports the language the user’s device is set to. For that reason all
        # reviews from Google Play will have their language set to ZZ.
        if self.country_iso == 'ZZ':
            self.country_iso = None

        self.version = json.get('version')
        self.date = parse(json.get('date'))
        self.product_id = six.u(str(json.get('product')))
        self.weight = int(json.get('weight'))
        self.id = six.u(str(json.get('id')))

    @property
    def country_available(self):
        return self.country_iso is not None

    @property
    def product(self):
        """
        Return the product that this PR is related to. This will hit the
        the API again.
        """
        raise NotImplementedError()

    @classmethod
    def is_valid_sort_key(cls, key):
        valid_keys = cls.SORT_FIELDS + ['-{}'.format(f) for f in cls.SORT_FIELDS]
        return key in valid_keys


class ReviewRating(base.AppFigureObject):

    def _load_from_json(self, json):
        self.stars = {}
        self.stars_total = 0

        for star, count in six.iteritems(json.get('stars', {})):
            self.stars[int(star)] = count
            self.stars_total += count

        self.versions = json.get('versions', {})
        self.countries = json.get('countries', {})
        self.products = json.get('products', {})
        self.languages = json.get('languages', {})
        self.tags = json.get('tags', {})

    @property
    def average_rating(self):
        if not self.stars_total:
            return None

        star_sum = sum([s * c for s, c in six.iteritems(self.stars)])
        return (D(star_sum) / D(self.stars_total)).quantize(D('0.1'))
