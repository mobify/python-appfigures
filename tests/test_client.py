# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import pytest
import betamax

from datetime import datetime
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

        assert product.has_metadata is False


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

        assert product.has_metadata is False


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

        assert product.has_metadata is False


@pytest.mark.integration
def test_retrieving_project_by_google_play_id_with_metadata(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('get_project_by_google_play_store_id_with_metadata'):  # noqa
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

        assert product.has_metadata is True
        assert sorted(product.metadata.keys()) == sorted(['en', 'ja'])

        assert product.metadata.en.all_rating == D('3.93')
        assert product.metadata.all_rating_count == 162814
        assert product.metadata.developer_email == 'android@rd.io'
        assert product.metadata.developer_site == 'http://www.rdio.com'
        assert product.metadata.downloads == '10000000-50000000'
        assert product.metadata.download_size == 13631488
        assert product.metadata.has_in_app_purchases is False
        assert product.metadata.name == 'Rdio Music'
        assert product.metadata.rating == 'Teen'
        assert product.metadata.top_developer is False
        assert product.metadata.view_url == 'https://play.google.com/store/apps/details?id=com.rdio.android.ui&hl=en'  # noqa

        assert product.metadata.ja.all_rating == D('3.94')

        with pytest.raises(AttributeError):
            product.metadata.de.all_rating


@pytest.mark.integration
def test_retrieve_reviews_for_app_store_product(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('retrieve_reviews_for_app_store_product'):
        reviews = client.find_reviews(products=[5555936])

        assert len(reviews) == 25

        review = reviews[0]
        assert review.product_id == '5555936'
        assert review.original_review == "The app crashes whenever it wants to and just stops playing the music and won't start again unless I restart the app. I also can't download songs when a station is playing because the music will crash and yet again I will have to restart the app. 5 star Amazing music service but just a mediocre 1 star app."  # noqa
        assert review.weight == 0
        assert review.title == 'Wow'
        assert review.review == "The app crashes whenever it wants to and just stops playing the music and won't start again unless I restart the app. I also can't download songs when a station is playing because the music will crash and yet again I will have to restart the app. 5 star Amazing music service but just a mediocre 1 star app."  # noqa
        assert review.author == 'Tony D'
        assert review.original_title == 'Wow'
        assert review.version == '3.6.2.83'
        assert review.country_iso is None
        assert review.country_available is False
        assert review.stars == D('2.00')
        assert review.date == datetime(2015, 9, 30, 3, 31, 49)
        assert review.id == '5555936L2RnbOL3Mz-NjX7wEuPpQIg'


@pytest.mark.integration
def test_review_ratings_for_single_product(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('test_ratings_for_single_product'):
        ratings = client.review_ratings(products=[39740449578])

        assert ratings.tags == {}

        assert sorted(ratings.countries.keys()) == sorted(['CA', 'US'])
        assert sorted(ratings.countries.values()) == sorted([225, 58])

        assert ratings.languages == {'N/A': 283}
        assert ratings.versions == {'N/A': 283}

        assert ratings.products == {'39740449578': 283}

        assert sorted(ratings.stars.keys()) == range(1, 6)
        assert sorted(ratings.stars.values()) == [16, 22, 30, 66, 149]

        assert ratings.stars_total == 283


@pytest.mark.integration
def test_generate_simple_sales_report_for_single_product(client):
    recorder = betamax.Betamax(client.session)

    with recorder.use_cassette('generate_sales_report_for_single_product'):
        report = client.simple_sales_report(products=[39740449578])

        assert report.revenue == D('0.00')
        assert report.gift_redemptions == 0
        assert report.downloads == 612271
        assert report.edu_downloads == 0
        assert report.returns == 0
        assert report.gifts == 0
        assert report.promos == 0
        assert report.updates == 2210231
        assert report.net_downloads == 612271
