# -*- coding: utf-8 -*-
'''
Script for generating Appfigures Oauth Tokens.

'''
import os
import sys
import urlparse

import requests
from appfigures.client import Client


OAUTH_BASE = Client.BASE_URL.add_path_segment('oauth')
OAUTH_REQUEST_TOKEN_URL = OAUTH_BASE.add_path_segment('request_token')
OAUTH_AUTHORIZE_URL = OAUTH_BASE.add_path_segment('authorize')
OAUTH_ACCESS_TOKEN_URL = OAUTH_BASE.add_path_segment('access_token')


def main():
    client_key = os.environ.get('APPFIGURES_CLIENT_KEY') or raw_input('Client Key: ')
    client_secret = os.environ.get('APPFIGURES_CLIENT_SECRET') or raw_input('Client Secret: ')

    oauth_request_token_response = requests.post(OAUTH_REQUEST_TOKEN_URL, data={
        'oauth_signature_method': 'PLAINTEXT',
        'oauth_callback': 'oob',
        'oauth_consumer_key': client_key,
        'oauth_signature': '{}&'.format(client_secret)
    })
    oauth_request_token_response.raise_for_status()
    oauth_request_token_params = dict(urlparse.parse_qsl(oauth_request_token_response.content))
    oauth_request_token = oauth_request_token_params['oauth_token']
    oauth_request_token_secret = oauth_request_token_params["oauth_token_secret"]

    oauth_authorize_url = OAUTH_AUTHORIZE_URL.append_query_param('oauth_token', oauth_request_token)
    print '--> {}'.format(oauth_authorize_url)
    oauth_verifier = raw_input("Verification Token: ")

    oauth_access_token_response = requests.post(OAUTH_ACCESS_TOKEN_URL, {
        'oauth_signature_method': 'PLAINTEXT',
        'oauth_verifier': oauth_verifier,
        'oauth_consumer_key': client_key,
        'oauth_token': oauth_request_token,
        'oauth_signature': '{}&{}'.format(client_secret, oauth_request_token_secret)
    })
    oauth_access_token_response.raise_for_status()
    oauth_request_token_params = dict(urlparse.parse_qsl(oauth_access_token_response.content))
    oauth_access_token = oauth_request_token_params['oauth_token']
    oauth_access_token_secret = oauth_request_token_params['oauth_token_secret']
    return oauth_access_token, oauth_access_token_secret


if __name__ == "__main__":
    oauth_access_token, oauth_access_token_secret = main()
    print 'OAUTH ACCESS TOKEN: {}'.format(oauth_access_token)
    print 'OAUTH ACCESS TOKEN SECRET: {}'.format(oauth_access_token_secret)