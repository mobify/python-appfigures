# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from decimal import Decimal as D


def as_int_or_none(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def as_decimal_or_none(value):
    try:
        return D(value)
    except (TypeError, ValueError):
        return None
