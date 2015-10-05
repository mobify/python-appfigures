# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import json

from decimal import Decimal as D

from appfigures.reports import SalesReport


def test_creating_sales_report_from_json():
    report_json = json.loads("""{
        "downloads": 155299,
        "updates": 91156,
        "returns": 56,
        "net_downloads": 155243,
        "promos": 2,
        "revenue": "26188.63",
        "edu_downloads": 54,
        "gifts": 36,
        "gift_redemptions": 0
    }""")

    report = SalesReport.from_json(report_json)

    assert report.downloads == 155299
    assert report.updates == 91156
    assert report.returns == 56
    assert report.net_downloads == 155243
    assert report.promos == 2
    assert report.revenue == D('26188.63')
    assert report.edu_downloads == 54
    assert report.gifts == 36
    assert report.gift_redemptions == 0
