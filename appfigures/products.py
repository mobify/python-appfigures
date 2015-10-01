# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from collections import namedtuple
from decimal import Decimal as D

from dateutil.parser import parse

from . import stores

Price = namedtuple('Price', ['value', 'currency'])


class Product(object):

    def __init__(self, json):
        super(Product, self).__init__()
        self._json_data = json

        if not json:
            return

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

    @classmethod
    def from_json(cls, json):
        return cls(json)

    def json(self):
        return self._json_data
