# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import requests

from purl import URL

from .decorators import cached_property
from .products import Product


class Client(object):
    BASE_URL = URL('https://api.appfigures.com/v2')

    def __init__(self, client_key, client_secret, oauth_token, oauth_secret,
                 signature_method='PLAINTEXT', timeout=5):
        self.client_key = client_key
        self.client_secret = client_secret
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret
        self.signature_method = signature_method
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update(self.auth_header)

    @cached_property
    def oauth_signature(self):
        return '{}&{}'.format(self.client_secret, self.oauth_secret)

    @cached_property
    def auth_header(self):
        auth_settings = [
            'oauth_signature_method={}'.format(self.signature_method),
            'oauth_consumer_key={}'.format(self.client_key),
            'oauth_token={}'.format(self.oauth_token),
            'oauth_signature={}'.format(self.oauth_signature)]

        return {'Authorization': 'OAuth {}'.format(', '.join(auth_settings))}

    def get_product(self, appfigures_id=None, store=None, product_id=None):
        if appfigures_id:
            return self._get_product_by_appfigures_id(appfigures_id)

        if store and product_id:
            return self._get_product_by_store_id(store, product_id)

        raise ParametersInvalid(
            "you have to provide an 'appfigure_id' or 'store' and 'product_id' "
            "parameters")

    def _get_product_by_appfigures_id(self, appfigures_id):
        """
        Retrieve the product with the AppFigures product ID `product_id`.
        """
        path = '/products/{appfigures_id}'.format(appfigures_id=appfigures_id)
        url = self.BASE_URL.add_path_segment(path)

        response = self.session.get(url.as_string(), timeout=self.timeout)

        if not response.ok:
            response.raise_for_status()

        return Product(response.json())

    def _get_product_by_store_id(self, store, product_id):
        """
        Retrieve the product with the store identifier and the store ID.
        """
        path = '/products/{store}/{product_id}'.format(store=store,
                                                       product_id=product_id)
        url = self.BASE_URL.add_path_segment(path)

        response = self.session.get(url.as_string(), timeout=self.timeout)

        if not response.ok:
            response.raise_for_status()

        return Product(response.json())

    def find_product(self, store, product_id):
        """
        Search

        """
