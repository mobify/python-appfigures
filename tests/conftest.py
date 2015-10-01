# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import pytest
import betamax

from appfigures.client import Client


CLIENT_KEY = os.getenv('CLIENT_KEY', '*' * 32)
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '*' * 32)
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN', '*' * 16)
OAUTH_SECRET = os.getenv('OAUTH_SECRET', '*' * 16)


with betamax.Betamax.configure() as config:
    cassette_dir = 'tests/cassettes/'
    if not os.path.exists(cassette_dir):
        os.makedirs(cassette_dir)
    config.cassette_library_dir = cassette_dir
    config.define_cassette_placeholder('<CLIENT_KEY>', CLIENT_KEY)
    config.define_cassette_placeholder('<CLIENT_SECRET>', CLIENT_SECRET)
    config.define_cassette_placeholder('<OAUTH_TOKEN>', OAUTH_TOKEN)
    config.define_cassette_placeholder('<OAUTH_SECRET>', OAUTH_SECRET)


@pytest.fixture
def client():
    return Client(client_key=CLIENT_KEY, client_secret=CLIENT_SECRET,
                  oauth_token=OAUTH_TOKEN, oauth_secret=OAUTH_SECRET)
