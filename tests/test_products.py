# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import json

from appfigures.products import Product


def test_creating_product_instance_from_json():
    json_data = json.loads(PRODUCT_GET_RESPONSE)
    product = Product.from_json(json_data)

    assert product.id == 212135374


PRODUCT_GET_RESPONSE = """{
  "id": 212135374,
  "name": "Rdio",
  "developer": "Rdio",
  "icon": "http://ecx.images-amazon.com/images/I/51IPlKhP19L._SL160_SL150_.png",
  "vendor_identifier": "B004T76OR8",
  "package_name": "B004T76OR8",
  "store_id": 3,
  "store": "amazon_appstore",
  "release_date": "2000-01-01T00:00:00",
  "added_date": "2012-05-30T19:16:43",
  "updated_date": "2013-07-02T21:00:00",
  "version": "2.6.3",
  "source": null,
  "type": "unknown",
  "devices": [
    "Handheld"
  ],
  "price": {
    "currency": "USD",
    "price": "0.00"
  }
}"""
