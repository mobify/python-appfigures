# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import pytest
import betamax

from decimal import Decimal as D

from appfigures import stores


@pytest.mark.integration
def test_retrieving_project_by_appfigures_id(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('get_project_by_appfigures_id'):
        product = client.get_product(appfigures_id='212135374')

        assert product.id == 212135374
        assert product.store == stores.AMAZON_APPSTORE
        assert product.developer == 'Rdio'
        assert product.price.currency == 'USD'
        assert product.price.value == D('0.0')
        assert product.store_id == 3
        assert product.version == '2.9'


@pytest.mark.integration
def test_retrieving_project_by_apple_store_id(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('get_project_by_apple_store_id'):
        product = client.get_product(store=stores.APPLE,
                                     product_id='335060889')

        assert product.id == 5985606
        assert product.store == stores.APPLE
        assert product.store_id == 1
        assert product.vendor_identifier == '335060889'
        assert product.developer == 'Rdio'
        assert product.price.currency == 'USD'
        assert product.price.value == D('0.0')
        assert product.version == '3.8.2'


@pytest.mark.integration
def test_retrieving_project_by_google_play_id(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('get_project_by_google_play_store_id'):
        product = client.get_product(store=stores.GOOGLE_PLAY,
                                     product_id='com.rdio.android.ui')

        print product.json()

        assert product.id == 5555936
        assert product.store == stores.GOOGLE_PLAY
        assert product.store_id == 2
        assert product.vendor_identifier == 'com.rdio.android.ui'
        assert product.developer == 'Rdio'
        assert product.price.currency == 'USD'
        assert product.price.value == D('0.0')
        assert product.version == 'Varies with device'
