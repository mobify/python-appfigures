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

        assert product.has_metadata == False


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

        assert product.has_metadata == False


@pytest.mark.integration
def test_retrieving_project_by_google_play_id(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('get_project_by_google_play_store_id'):
        product = client.get_product(store=stores.GOOGLE_PLAY,
                                     product_id='com.rdio.android.ui')

        assert product.id == 5555936
        assert product.store == stores.GOOGLE_PLAY
        assert product.store_id == 2
        assert product.vendor_identifier == 'com.rdio.android.ui'
        assert product.developer == 'Rdio'
        assert product.price.currency == 'USD'
        assert product.price.value == D('0.0')
        assert product.version == 'Varies with device'

        assert product.has_metadata == False


@pytest.mark.integration
def test_retrieving_project_by_google_play_id_with_metadata(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('get_project_by_google_play_store_id_with_metadata'):
        product = client.get_product(store=stores.GOOGLE_PLAY,
                                     product_id='com.rdio.android.ui',
                                     include_metadata=True)

        assert product.id == 5555936
        assert product.store == stores.GOOGLE_PLAY
        assert product.store_id == 2
        assert product.vendor_identifier == 'com.rdio.android.ui'
        assert product.developer == 'Rdio'
        assert product.price.currency == 'USD'
        assert product.price.value == D('0.0')

        assert product.has_metadata == True
        assert product.metadata.keys() == ['en', 'ja']

        assert product.metadata.en.all_rating == D('3.93')
        assert product.metadata.all_rating_count == 162814
        assert product.metadata.developer_email == 'android@rd.io'
        assert product.metadata.developer_site == 'http://www.rdio.com'
        assert product.metadata.downloads == '10000000-50000000'
        assert product.metadata.download_size == 13631488
        assert product.metadata.has_in_app_purchases == False
        assert product.metadata.name == 'Rdio Music'
        assert product.metadata.rating == 'Teen'
        assert product.metadata.top_developer == False
        assert product.metadata.view_url == 'https://play.google.com/store/apps/details?id=com.rdio.android.ui&hl=en'

        assert product.metadata.ja.all_rating == D('3.94')

        with pytest.raises(AttributeError):
            product.metadata.de.all_rating
