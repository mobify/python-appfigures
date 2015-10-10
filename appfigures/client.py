# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import six
import requests

from purl import URL

from . import base
from . import reports
from .decorators import cached_property
from .products import Product
from .reviews import ReviewCollection, Review, ReviewRating
from .exceptions import ParametersInvalid


class Client(object):
    BASE_URL = URL('https://api.appfigures.com/v2')

    def __init__(self, client_key, client_secret, oauth_token, oauth_secret,
                 signature_method='PLAINTEXT', timeout=10):
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

    def get_product(self, appfigures_id=None, store=None, product_id=None,
                    include_metadata=False):
        if appfigures_id:
            return self._get_product_by_appfigures_id(
                appfigures_id,
                include_metadata=include_metadata)

        if store and product_id:
            return self._get_product_by_store_id(
                store,
                product_id,
                include_metadata=include_metadata)

        raise ParametersInvalid(
            "you have to provide an 'appfigure_id' or 'store' and 'product_id' "
            "parameters")

    def find_product(self, term, filter, page, count=25):
        raise NotImplementedError()

    def find_product_by_developer(self, developer, filter, page, count=25):
        term = '@developer={}'.format(developer)
        return self.find_product(term, filter, page, count)

    def find_product_by_name(self, name, filter, page, count=25):
        term = '@name={}'.format(name)
        return self.find_product(term, filter, page, count)

    def _get_product_by_appfigures_id(self, appfigures_id,
                                      include_metadata=False):
        """
        Retrieve the product with the AppFigures product ID `product_id`.
        """
        path = 'products/{appfigures_id}'.format(appfigures_id=appfigures_id)
        url = self.BASE_URL.add_path_segment(path)

        query_params = {}
        if include_metadata:
            query_params['meta'] = True

        response = self.session.get(url.as_string(),
                                    timeout=self.timeout,
                                    params=query_params)

        if not response.ok:
            response.raise_for_status()

        return Product(response.json())

    def _get_product_by_store_id(self, store, product_id,
                                 include_metadata=False):
        """
        Retrieve the product with the store identifier and the store ID.
        """
        path = 'products/{store}/{product_id}'.format(store=store,
                                                      product_id=product_id)

        url = self.BASE_URL.add_path_segment(path)

        query_params = {}
        if include_metadata:
            query_params['meta'] = 'true'

        response = self.session.get(url.as_string(),
                                    timeout=self.timeout,
                                    params=query_params)

        if not response.ok:
            response.raise_for_status()

        return Product(response.json())

    def find_reviews(self, query=None, products=None, countries=None, page=1,
                     count=500, lang=None, author=None, versions=None,
                     stars=None, sort=None, start=None, end=None):
        """
        Find reviews matching the parameters.

        `appfigures API Documentation
        <http://docs.appfigures.com/api/reference/v2/reviews>`

        Args:
            query: Filter by reviews matching this query string.
            products: Filter by reviews matching this list of product ids.
            countries: Filter by countries matching this list of country isos.
            lang: Translate reviews into this language.
            author: Filter by reviews matching this author string.
            versions: Filter by reviews matching this list of versions.
            stars: Filter by reviews matching this list of stars.
            sort: How to soort reviews.
            start: Filter by reviews created after this datetime.
            end: Filter by reviews created before this datetime.

        Returns:
            A `ReviewCollection <appfigures.reviews.ReviewCollection` instance.

        Raises:
            ParametersInvalid: An invalid parameter for the API is provided.
            HTTPError: The API call returned a status code that's not `200 OK`.
        """
        if 1 > count > 501:
            raise ParametersInvalid(
                'count parameter must be between 1 and 500')

        if sort and not Review.is_valid_sort_key(sort):
            raise ParametersInvalid(
                'key {} is not a valid sort key, only {} are allowed'.format(
                    sort, Review.SORT_FIELDS))

        url = self.BASE_URL.add_path_segment('reviews')

        query_params = {'page': page,
                        'count': count}

        if query:
            query_params['q'] = query

        if products:
            query_params['products'] = self._iter_to_query_param(products)

        if countries:
            query_params['countries'] = self._iter_to_query_param(countries)

        if lang:
            query_params['lang'] = self._iter_to_query_param(lang)

        if versions:
            query_params['versions'] = self._iter_to_query_param(versions)

        if stars:
            query_params['stars'] = self._iter_to_query_param(stars)

        if author:
            query_params['author'] = author

        if sort:
            query_params['sort'] = sort

        if start:
            query_params['start'] = start.strftime(base.QUERY_DATE_FORMAT)

        if end:
            query_params['end'] = end.strftime(base.QUERY_DATE_FORMAT)

        response = self.session.get(url.as_string(),
                                    timeout=self.timeout,
                                    params=query_params)

        if not response.ok:
            response.raise_for_status()

        return ReviewCollection(response.json())

    def review_ratings(self, query=None, products=None, countries=None,
                       author=None, versions=None, stars=None,
                       start_date=None, end_date=None):

        url = self.BASE_URL.add_path_segment('reviews/count')

        query_params = {}

        if products:
            query_params['products'] = self._iter_to_query_param(products)

        if query:
            query_params['q'] = query

        if countries:
            query_params['countries'] = self._iter_to_query_param(countries)

        if author:
            query_params['author'] = author

        if versions:
            query_params['versions'] = self._iter_to_query_param(versions)

        if stars:
            query_params['start'] = self._iter_to_query_param(stars)

        if start_date:
            query_params['start'] = start_date.strftime(base.QUERY_DATE_FORMAT)

        if end_date:
            query_params['end'] = end_date.strftime(base.QUERY_DATE_FORMAT)

        response = self.session.get(url.as_string(),
                                    timeout=self.timeout,
                                    params=query_params)

        if not response.ok:
            response.raise_for_status()

        return ReviewRating(response.json())

    def simple_sales_report(self, products=None, countries=None,
                            include_inapps=False,
                            start_date=None, end_date=None,
                            granularity=reports.Granularity.DAILY):
        """
        Generate a simple sales report for all or a subset of products.

        `appfigures API Documentation
        <http://docs.appfigures.com/api/reference/v2/sales#Getting_Simple_Totals>`

        Args:
            products: A list of appfigure product IDs.
            countries: A list of ISO-3166-1 alpha-2 ISO codes.
            include_inapps: A boolean to indicate if children of the app should
                be included in the report (defaut: `False`).
            start_date: The date to generate the report **from** in YYYY-MM-DD
                format. The date is included in the report.
            end_date: The date to generate the report **to** in YYYY-MM-DD
                format. The date is included in the report.
            granularity: A valid `Granularity` value describing how dates are
                aggregate in the report (default: `daily`).

        Returns:
            A `SalesReport <appfigures.reports.SalesReport` instance.

        Raises:
            ParametersInvalid: An invalid parameter for the API is provided.
            HTTPError: The API call returned a status code that's not `200 OK`.
        """
        url = self.BASE_URL.add_path_segment('reports/sales')

        query_params = {}

        if products:
            query_params['products'] = self._iter_to_query_param(products)

        if countries:
            query_params['countries'] = self._iter_to_query_param(countries)

        if include_inapps:
            query_params['include_inapps'] = 'true'

        if granularity and reports.Granularity.validate(granularity):
            query_params['granularity'] = granularity

        if start_date:
            query_params['start_date'] = start_date.strftime(
                base.QUERY_DATE_FORMAT)

        if end_date:
            query_params['end_date'] = end_date.strftime(base.QUERY_DATE_FORMAT)

        response = self.session.get(url.as_string(),
                                    timeout=self.timeout,
                                    params=query_params)

        if not response.ok:
            response.raise_for_status()

        return reports.SalesReport(response.json())

    def _iter_to_query_param(self, iterable):
        return ','.join([six.u(str(i)) for i in iterable])
