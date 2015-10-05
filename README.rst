python-appfigures
#############################


.. image:: https://travis-ci.org/mobify/python-appfigures.svg?branch=master
   :target: https://travis-ci.org/mobify/python-appfigures


**Disclaimer**: This project is under active development and currently provides
an incomplete implementation of an API wrapper for the AppFigures API.


Installation
============

This package is currently not available on PyPI (yet). For new, you'll have to
install it using the git repo URL::

    $ pip install -e https://github.com/mobify/python-appfigures.git#egg=python-appfigures-dev

This will install the package in "editing mode" which will ensure that you'll
be able to get the latest changes from git when you update you installation.


Quickstart
==========

For now, you'll have to create your OAuth token and secret manually. Assuming
you have your API and OAuth credentials available, you can access the
AppFigures API like this::

    from appfigures import stores
    from appfigures.client import Client

    # create new API client instance
    app_figures = Client(client_key=CLIENT_KEY,
                         client_secret=CLIENT_SECRET,
                         oauth_token=OAUTH_TOKEN,
                         oauth_secret=OAUTH_SECRET)

    # retrieve a specific product
    product = app_figures.get_product(store=stores.APPLE,
                                      product_id='335060889')


Development
===========

Install the project and all its requirements in development mode:

.. code:: bash

    $ pip install -e ".[test]"


License
=======

This code is licensed under the `MIT License`_.

.. _`MIT License`: https://github.com/mobify/python-appfigures/blob/master/LICENSE
