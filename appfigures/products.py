# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import six

from collections import namedtuple
from decimal import Decimal as D

from dateutil.parser import parse

from . import base
from . import stores
from . import devices

Price = namedtuple('Price', ['value', 'currency'])


class Product(base.AppFigureObject):

    def _load_from_json(self, json):
        self.id = json.get('id')
        self.name = json.get('name')
        self.developer = json.get('developer')
        self.icon = json.get('icon')
        self.vendor_identifier = json.get('vendor_identifier')
        self.package_name = json.get('package_name')

        self.store = json.get('store')
        self.store_id = json.get('store_id')

        self.sku = json.get('sku')
        self.ref_no = json.get('ref_no')
        self.vendor_identifier = json.get('vendor_identifier')

        self.release_date = parse(json.get('release_date'))
        self.added_date = parse(json.get('added_date'))
        self.updated_date = parse(json.get('updated_date'))

        self.version = json.get('version')
        if self.version:
            self.version = self.version.strip()

        self.source = json.get('source')
        self.type = json.get('type')
        self.devices = json.get('devices', [])

        price = json.get('price')
        if not price:
            self.price = None

        try:
            self.price = Price(D(price.get('price')), price.get('currency'))
        except (InvalidOperation, ValueError):
            self.price = None

        meta_json = json.get('meta', {})
        self.metadata = ProductMetadataCollection.from_json(meta_json)

    @property
    def is_handheld(self):
        return devices.HANDHELD in self.devices

    @property
    def is_tablet(self):
        return devices.TABLET in self.devices

    @property
    def is_desktop(self):
        return devices.DESKTOP in self.devices

    @property
    def has_metadata(self):
        return len(self.metadata) > 0

    @classmethod
    def from_json(cls, json):
        return cls(json)

    def json(self):
        return self._json_data


class ProductMetadataCollection(dict):
    DEFAULT_LANGUAGE = 'en'

    def __init__(self, json):
        for language, metadata in six.iteritems(json):
            self[language] = ProductMetadata.from_json(language, metadata)

    def __getattr__(self, key):
        """
        Expose the language metadata as attributes and allow direct access
        to attributes of the english language metadata if it is present.
        """
        if key in self:
            return self[key]
        elif hasattr(self[self.DEFAULT_LANGUAGE], key):
            return getattr(self[self.DEFAULT_LANGUAGE], key)
        raise AttributeError()

    @classmethod
    def from_json(cls, json):
        return cls(json)


class ProductMetadata(base.AppFigureObject):

    def __init__(self, language, json):
        self.language = language
        super(ProductMetadata, self).__init__(json)

    def _load_from_json(self, json):
        self.all_rating = D(json.get('all_rating'))
        self.all_rating_count = int(json.get('all_rating_count'))
        self.description = json.get('description')
        self.developer_email = json.get('developer_email')
        self.developer_site = json.get('developer_site')
        self.downloads = json.get('downloads')

        try:
            self.download_size = int(json.get('download_size'))
        except (ValueError, TypeError):
            self.download_size = None

        self.has_in_app_purchases = (json.get('has_inapps') == 'true')
        self.name = json.get('name')
        self.rating = json.get('rating')
        self.release_notes = json.get('release_notes')
        self.top_developer = (json.get('top_developer') == 'true')
        self.view_url = json.get('view_url')

    @classmethod
    def from_json(cls, language, json):
        flattened_json = {}
        for data in json:
            if data.get('language') != language:
                continue
            flattened_json[data.get('key')] = data.get('value')

        return cls(language, flattened_json)
